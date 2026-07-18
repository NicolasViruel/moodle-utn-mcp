import assert from "node:assert/strict";
import test from "node:test";
import { MOODLE_ORIGINS, assertAllowedOrigin, classifyResponse, probeCapabilities, redactUrl } from "../probe.js";

test("allows exactly the two hard-coded UTN Moodle origins", () => {
  for (const origin of MOODLE_ORIGINS) {
    assert.equal(assertAllowedOrigin(origin).origin, origin);
  }
  assert.throws(() => assertAllowedOrigin("https://example.com"), /hard-coded UTN Moodle origins/);
});

test("redacts URL query values from diagnostics", () => {
  assert.equal(
    redactUrl("https://tup.sied.utn.edu.ar/login/index.php?token=secret&x=1"),
    "https://tup.sied.utn.edu.ar/login/index.php"
  );
});

test("classifies expected public endpoint responses", () => {
  assert.equal(classifyResponse("/login/index.php", 200), "reachable");
  assert.equal(classifyResponse("/login/index.php", 401), "requires_authentication_or_parameters");
  assert.equal(classifyResponse("/login/index.php", 404), "not_available");
  assert.equal(classifyResponse("/", 302, "/login/index.php?session=private"), "redirects_to_login");
  assert.equal(classifyResponse("/", 500), "unexpected_response");
});

test("stops reading a response stream at the body byte ceiling", async () => {
  const originalFetch = globalThis.fetch;
  const encoder = new TextEncoder();
  const firstChunk = encoder.encode(`Moodle${" ".repeat(8_186)}`);
  let rootStreamPulls = 0;

  globalThis.fetch = async (input) => {
    const url = new URL(input.toString());
    if (url.pathname !== "/") {
      return new Response("ok", { status: 200 });
    }

    return new Response(new ReadableStream<Uint8Array>({
      pull(controller) {
        rootStreamPulls += 1;
        if (rootStreamPulls === 1) {
          controller.enqueue(firstChunk);
          return;
        }
        controller.enqueue(encoder.encode("this body content exceeds the ceiling"));
        controller.close();
      }
    }, { highWaterMark: 0 }), { status: 200 });
  };

  try {
    const report = await probeCapabilities();
    assert.equal(report.moodle.detected, true);
    assert.equal(rootStreamPulls, 1);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
