import assert from "node:assert/strict";
import test from "node:test";
import { MoodleRestClient, MoodleRestError, optionalRestClient } from "../moodle-rest.js";

const environment = { MOODLE_REST_ORIGIN: "https://tup.sied.utn.edu.ar", MOODLE_REST_TOKEN: "test-token-only" };

test("REST mode requires both environment variables and the exact approved origin", () => {
  assert.equal(MoodleRestClient.fromEnvironment({ MOODLE_REST_ORIGIN: "https://tup.sied.utn.edu.ar" }), undefined);
  assert.equal(MoodleRestClient.fromEnvironment({ MOODLE_REST_ORIGIN: "https://example.com", MOODLE_REST_TOKEN: "x" }), undefined);
  assert.equal(MoodleRestClient.fromEnvironment({ MOODLE_REST_ORIGIN: "https://tup.sied.utn.edu.ar/other", MOODLE_REST_TOKEN: "x" }), undefined);
  assert.throws(() => optionalRestClient({}), /Optional REST mode is disabled/);
});

test("REST calls use the fixed endpoint and never put the token in the URL", async () => {
  let request: Request | undefined;
  const client = MoodleRestClient.fromEnvironment(environment, async (input, init) => {
    request = new Request(input, init);
    return Response.json({ userid: 7 });
  });
  assert.ok(client);
  await client.siteInfo();
  assert.equal(request?.url, "https://tup.sied.utn.edu.ar/webservice/rest/server.php");
  assert.equal(request?.method, "POST");
  const body = await request?.text();
  assert.match(body ?? "", /wstoken=test-token-only/);
  assert.doesNotMatch(request?.url ?? "", /test-token-only/);
});

test("normalizes Moodle and malformed-response errors without echoing sensitive payloads", async () => {
  const moodleError = MoodleRestClient.fromEnvironment(environment, async () => Response.json({ exception: "invalid_response_exception", errorcode: "invalidtoken", message: "test-token-only" }));
  assert.ok(moodleError);
  await assert.rejects(moodleError.siteInfo(), (error: unknown) => error instanceof MoodleRestError && !error.message.includes("test-token-only"));
  const malformed = MoodleRestClient.fromEnvironment(environment, async () => new Response("not json", { status: 200 }));
  assert.ok(malformed);
  await assert.rejects(malformed.siteInfo(), /malformed JSON/);
});

test("maps courses, deadlines, content, grades, and forums from Moodle responses", async () => {
  let request: Request | undefined;
  const responses = [
    { userid: 7 },
    [{ id: 42, fullname: "Algorithms", shortname: "ALG" }],
    { events: [{ id: 1, name: "Assignment", courseid: 42, timestart: 1_800_000_000, eventtype: "due", description: "Submit" }] },
    [{ id: 5, name: "Week 1", modules: [{ id: 6, name: "Slides", modname: "resource", visible: 1 }] }],
    { userid: 7 },
    { usergrades: [{ gradeitems: [{ itemname: "Assignment", gradeformatted: "9", percentageformatted: "90%", feedback: "Good" }] }] },
    [{ id: 9, name: "Announcements", type: "news", intro: "Updates", course: 42 }]
  ];
  const client = MoodleRestClient.fromEnvironment(environment, async (input, init) => {
    request = new Request(input, init);
    return Response.json(responses.shift());
  });
  assert.ok(client);
  assert.deepEqual(await client.myCourses(), [{ id: 42, name: "Algorithms", shortName: "ALG" }]);
  assert.deepEqual(await client.upcomingDeadlines(), [{ id: 1, title: "Assignment", courseId: 42, dueAt: 1_800_000_000, type: "due", description: "Submit" }]);
  const deadlineParams = new URLSearchParams(await request?.text());
  assert.equal(deadlineParams.get("options[limitnum]"), "100");
  assert.ok(deadlineParams.get("options[timestart]") && deadlineParams.get("options[timeend]"));
  assert.equal(deadlineParams.get("events[timestart]"), null);
  assert.deepEqual(await client.courseContent(42), [{ id: 5, name: "Week 1", summary: undefined, modules: [{ id: 6, name: "Slides", type: "resource", visible: true, description: undefined }] }]);
  assert.deepEqual(await client.courseGrades(42), [{ itemName: "Assignment", grade: "9", percentage: "90%", feedback: "Good", feedbackFormat: undefined }]);
  assert.deepEqual(await client.courseForums(42), [{ id: 9, name: "Announcements", type: "news", intro: "Updates", courseId: 42 }]);
});
