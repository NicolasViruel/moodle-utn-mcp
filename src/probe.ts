export const MOODLE_ORIGINS = [
  "https://tup.sied.utn.edu.ar",
  "https://utnsannicolas.quinttos.com"
] as const;
export const MOODLE_ORIGIN = MOODLE_ORIGINS[0];
export const QUINTTOS_LOGIN_URL = "https://utnsannicolas.quinttos.com/index.php/login";

const REQUEST_TIMEOUT_MS = 5_000;
const MAX_BODY_BYTES = 8_192;

export type EndpointClassification =
  | "reachable"
  | "redirects_to_login"
  | "requires_authentication_or_parameters"
  | "not_available"
  | "unexpected_response"
  | "network_unavailable";

export interface EndpointEvidence {
  endpoint: string;
  classification: EndpointClassification;
  status?: number;
  contentType?: string;
  location?: string;
  detail: string;
}

export interface CapabilityReport {
  origin: string;
  checkedAt: string;
  moodle: {
    detected: boolean;
    versionHint?: string;
  };
  endpoints: EndpointEvidence[];
  recommendedNextStep: string;
}

export function assertAllowedOrigin(origin: string): URL {
  const url = new URL(origin);
  if (!MOODLE_ORIGINS.includes(url.origin as typeof MOODLE_ORIGINS[number])) {
    throw new Error("Only the hard-coded UTN Moodle origins are allowed.");
  }
  return url;
}

export function redactUrl(value: string): string {
  try {
    const url = new URL(value, MOODLE_ORIGIN);
    return `${url.origin}${url.pathname}`;
  } catch {
    return "[unparseable URL redacted]";
  }
}

export function classifyResponse(endpoint: string, status: number, location?: string): EndpointClassification {
  if (status >= 200 && status < 300) {
    return "reachable";
  }
  if (status >= 300 && status < 400 && location?.includes("/login/")) {
    return "redirects_to_login";
  }
  if (status === 401 || status === 403 || status === 405 || status === 400) {
    return "requires_authentication_or_parameters";
  }
  if (status === 404 || status === 410) {
    return "not_available";
  }
  return "unexpected_response";
}

function extractMoodleIdentity(body: string): { detected: boolean; versionHint?: string } {
  const detected = /moodle/i.test(body);
  const version = body.match(/Moodle\s+(\d+(?:\.\d+){1,3})/i)?.[1];
  return version ? { detected: true, versionHint: version } : { detected };
}

async function readLimitedBody(response: Response): Promise<string> {
  if (!response.body) {
    return "";
  }

  const reader = response.body.getReader();
  const chunks: Uint8Array[] = [];
  let bytesRead = 0;

  try {
    while (bytesRead < MAX_BODY_BYTES) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }

      const bytesToKeep = Math.min(value.byteLength, MAX_BODY_BYTES - bytesRead);
      chunks.push(value.slice(0, bytesToKeep));
      bytesRead += bytesToKeep;
    }
  } finally {
    await reader.cancel().catch(() => undefined);
  }

  const body = new Uint8Array(bytesRead);
  let offset = 0;
  for (const chunk of chunks) {
    body.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return new TextDecoder().decode(body);
}

async function probeEndpoint(origin: string, endpoint: string): Promise<{ evidence: EndpointEvidence; body?: string }> {
  const url = new URL(endpoint, assertAllowedOrigin(origin));
  try {
    const response = await fetch(url, {
      method: "GET",
      redirect: "manual",
      signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
      headers: { Accept: "text/html,application/json;q=0.9,*/*;q=0.1" }
    });
    const location = response.headers.get("location") ?? undefined;
    const contentType = response.headers.get("content-type")?.split(";", 1)[0];
    const body = await readLimitedBody(response);
    const classification = classifyResponse(endpoint, response.status, location);
    return {
      evidence: {
        endpoint,
        classification,
        status: response.status,
        contentType,
        location: location ? redactUrl(location) : undefined,
        detail: `Public GET returned HTTP ${response.status}.`
      },
      body
    };
  } catch (error) {
    const detail = error instanceof Error && error.name === "TimeoutError"
      ? `Public GET timed out after ${REQUEST_TIMEOUT_MS} ms.`
      : "Public GET could not reach the endpoint.";
    return {
      evidence: { endpoint, classification: "network_unavailable", detail }
    };
  }
}

export async function probeCapabilities(origin = MOODLE_ORIGIN): Promise<CapabilityReport> {
  assertAllowedOrigin(origin);
  const root = await probeEndpoint(origin, "/");
  const login = await probeEndpoint(origin, "/login/index.php");
  const moodle = extractMoodleIdentity(root.body ?? "");

  return {
    origin: MOODLE_ORIGIN,
    checkedAt: new Date().toISOString(),
    moodle,
    endpoints: [root.evidence, login.evidence],
    recommendedNextStep: "Use the local browser-login tool for a user-operated session. Do not submit credentials through this probe."
  };
}
