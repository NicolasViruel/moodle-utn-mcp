import { MOODLE_ORIGIN } from "./probe.js";

const REST_PATH = "/webservice/rest/server.php";
const REQUEST_TIMEOUT_MS = 10_000;
const REST_ORIGIN_ENV = "MOODLE_REST_ORIGIN";
const REST_TOKEN_ENV = "MOODLE_REST_TOKEN";
const LEGACY_ORIGIN_ENV = "MOODLE_URL";
const LEGACY_TOKEN_ENV = "MOODLE_TOKEN";

type Environment = Record<string, string | undefined>;
type Fetcher = typeof fetch;

export interface MoodleRestStatus {
  available: boolean;
  detail: string;
  origin?: string;
}

export class MoodleRestError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "MoodleRestError";
  }
}

function envValue(environment: Environment, ...keys: string[]): string | undefined {
  for (const key of keys) {
    const value = environment[key]?.trim();
    if (value) return value;
  }
  return undefined;
}

function configuredOrigin(environment: Environment): URL | undefined {
  const origin = envValue(environment, REST_ORIGIN_ENV, LEGACY_ORIGIN_ENV);
  const token = envValue(environment, REST_TOKEN_ENV, LEGACY_TOKEN_ENV);
  if (!origin || !token) return undefined;

  try {
    const url = new URL(origin);
    if (url.origin !== MOODLE_ORIGIN || url.pathname !== "/" || url.search || url.hash) return undefined;
    return url;
  } catch {
    return undefined;
  }
}

function configuredToken(environment: Environment): string | undefined {
  return configuredOrigin(environment) ? envValue(environment, REST_TOKEN_ENV, LEGACY_TOKEN_ENV) : undefined;
}

function appendFormValue(body: URLSearchParams, key: string, value: unknown): void {
  if (value === undefined || value === null) return;
  if (Array.isArray(value)) {
    value.forEach((entry, index) => appendFormValue(body, `${key}[${index}]`, entry));
  } else if (typeof value === "object") {
    for (const [childKey, childValue] of Object.entries(value)) {
      appendFormValue(body, `${key}[${childKey}]`, childValue);
    }
  } else {
    body.append(key, String(value));
  }
}

function unavailable(): MoodleRestStatus {
  return {
    available: false,
    detail: `Optional REST mode is disabled. Set ${REST_ORIGIN_ENV} (or ${LEGACY_ORIGIN_ENV}) to the approved Moodle origin and ${REST_TOKEN_ENV} (or ${LEGACY_TOKEN_ENV}) in .env or the MCP process environment. Browser tools remain separate and available.`
  };
}

function normalizeMoodleError(payload: unknown): MoodleRestError | undefined {
  if (!payload || typeof payload !== "object") return undefined;
  const record = payload as Record<string, unknown>;
  if (typeof record.exception !== "string") return undefined;

  const errorCode = typeof record.errorcode === "string" ? record.errorcode : "";
  if (/servicenotavailable|accessexception|nopermissions|invalidtoken|invalidparameter/i.test(errorCode)) {
    return new MoodleRestError("This Moodle site does not make the required read-only web-service function available to this token.");
  }
  return new MoodleRestError("Moodle rejected the read-only web-service request.");
}

function asRecord(value: unknown, functionName: string): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new MoodleRestError(`Moodle returned an unexpected response for ${functionName}.`);
  }
  return value as Record<string, unknown>;
}

function asArray(value: unknown): Record<string, unknown>[] {
  return Array.isArray(value) ? value.filter((item): item is Record<string, unknown> => Boolean(item) && typeof item === "object" && !Array.isArray(item)) : [];
}

function text(value: unknown): string | undefined {
  return typeof value === "string" && value.trim() ? value : undefined;
}

function number(value: unknown): number | undefined {
  return typeof value === "number" && Number.isFinite(value) ? value : undefined;
}

export class MoodleRestClient {
  private constructor(private readonly endpoint: URL, private readonly token: string, private readonly fetcher: Fetcher) {}

  static fromEnvironment(environment: Environment = process.env, fetcher: Fetcher = fetch): MoodleRestClient | undefined {
    const origin = configuredOrigin(environment);
    const token = configuredToken(environment);
    return origin && token ? new MoodleRestClient(new URL(REST_PATH, origin), token, fetcher) : undefined;
  }

  static status(environment: Environment = process.env): MoodleRestStatus {
    const origin = configuredOrigin(environment);
    return origin ? { available: true, origin: origin.origin, detail: "Optional REST mode is configured. It uses its own token and does not use the browser session." } : unavailable();
  }

  async call(functionName: string, params: Record<string, unknown> = {}): Promise<unknown> {
    const body = new URLSearchParams({ wstoken: this.token, wsfunction: functionName, moodlewsrestformat: "json" });
    for (const [key, value] of Object.entries(params)) appendFormValue(body, key, value);

    let response: Response;
    try {
      response = await this.fetcher(this.endpoint, {
        method: "POST",
        redirect: "error",
        signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
        headers: { Accept: "application/json", "Content-Type": "application/x-www-form-urlencoded" },
        body
      });
    } catch (error) {
      if (error instanceof Error && error.name === "TimeoutError") {
        throw new MoodleRestError(`Moodle REST did not respond within ${REQUEST_TIMEOUT_MS / 1_000} seconds.`);
      }
      throw new MoodleRestError("Moodle REST could not be reached.");
    }
    if (!response.ok) throw new MoodleRestError(`Moodle REST returned HTTP ${response.status}.`);

    let payload: unknown;
    try {
      payload = await response.json();
    } catch {
      throw new MoodleRestError("Moodle REST returned malformed JSON.");
    }
    const moodleError = normalizeMoodleError(payload);
    if (moodleError) throw moodleError;
    return payload;
  }

  async siteInfo(): Promise<Record<string, unknown>> {
    return asRecord(await this.call("core_webservice_get_site_info"), "core_webservice_get_site_info");
  }

  async myCourses(): Promise<Record<string, unknown>[]> {
    const info = await this.siteInfo();
    const userId = number(info.userid);
    if (!userId) throw new MoodleRestError("Moodle REST did not return the current user identity.");
    const response = await this.call("core_enrol_get_users_courses", { userid: userId });
    return asArray(response).map((course) => ({ id: number(course.id), name: text(course.fullname) ?? text(course.shortname), shortName: text(course.shortname) })).filter((course) => course.id && course.name);
  }

  async upcomingDeadlines(): Promise<Record<string, unknown>[]> {
    const now = Math.floor(Date.now() / 1_000);
    const response = asRecord(await this.call("core_calendar_get_calendar_events", { options: { timestart: now, timeend: now + 90 * 24 * 60 * 60, limitnum: 100 } }), "core_calendar_get_calendar_events");
    return asArray(response.events).map((event) => ({ id: number(event.id), title: text(event.name), courseId: number(event.courseid), dueAt: number(event.timestart), type: text(event.eventtype), description: text(event.description) })).filter((event) => event.title && event.dueAt);
  }

  async courseContent(courseId: number): Promise<Record<string, unknown>[]> {
    const response = await this.call("core_course_get_contents", { courseid: courseId });
    return asArray(response).map((section) => ({ id: number(section.id), name: text(section.name), summary: text(section.summary), modules: asArray(section.modules).map((module) => ({ id: number(module.id), name: text(module.name), type: text(module.modname), visible: module.visible === 1, description: text(module.description) })) }));
  }

  async courseGrades(courseId: number): Promise<Record<string, unknown>[]> {
    const info = await this.siteInfo();
    const userId = number(info.userid);
    if (!userId) throw new MoodleRestError("Moodle REST did not return the current user identity.");
    const response = asRecord(await this.call("gradereport_user_get_grade_items", { courseid: courseId, userid: userId }), "gradereport_user_get_grade_items");
    return asArray(response.usergrades).flatMap((grade) => asArray(grade.gradeitems)).map((item) => ({ itemName: text(item.itemname), grade: text(item.gradeformatted), percentage: text(item.percentageformatted), feedback: text(item.feedback), feedbackFormat: number(item.feedbackformat) })).filter((item) => item.itemName);
  }

  async courseForums(courseId: number): Promise<Record<string, unknown>[]> {
    const response = await this.call("mod_forum_get_forums_by_courses", { courseids: [courseId] });
    return asArray(response).map((forum) => ({ id: number(forum.id), name: text(forum.name), type: text(forum.type), intro: text(forum.intro), courseId: number(forum.course) })).filter((forum) => forum.id && forum.name);
  }
}

export function optionalRestClient(environment: Environment = process.env, fetcher: Fetcher = fetch): MoodleRestClient {
  const client = MoodleRestClient.fromEnvironment(environment, fetcher);
  if (!client) throw new MoodleRestError(unavailable().detail);
  return client;
}
