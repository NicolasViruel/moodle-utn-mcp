import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { probeCapabilities } from "./probe.js";
import { MoodleBrowserSession } from "./browser-session.js";
import { MoodleRestClient, optionalRestClient } from "./moodle-rest.js";
import { loadProjectEnv } from "./load-env.js";

loadProjectEnv();

const server = new McpServer({
  name: "moodle-utn-mcp",
  version: "0.1.0"
});
const browserSession = new MoodleBrowserSession();
const courseIdSchema = z.number().int().positive().describe("Numeric Moodle course id returned by moodle_rest_my_courses");

server.registerTool(
  "moodle_probe_capabilities",
  {
    title: "Probe UTN Moodle public capabilities",
    description: "Performs read-only unauthenticated GET requests against the fixed UTN Moodle origin. It accepts no credentials, tokens, URLs, or origins."
  },
  async () => ({
    content: [{ type: "text", text: JSON.stringify(await probeCapabilities(), null, 2) }]
  })
);

server.registerTool(
  "moodle_rest_status",
  {
    title: "Check optional Moodle REST mode",
    description: "Reports whether the separately configured, token-based read-only REST mode is available. It does not inspect or expose the token and does not use the browser session."
  },
  async () => ({ content: [{ type: "text", text: JSON.stringify(MoodleRestClient.status(), null, 2) }] })
);

server.registerTool(
  "moodle_rest_my_courses",
  {
    title: "List my Moodle courses via REST",
    description: "Uses only the optional environment-configured REST token to list the current user's courses. It has no inputs, performs no writes, and is separate from the browser session."
  },
  async () => ({ content: [{ type: "text", text: JSON.stringify({ courses: await optionalRestClient().myCourses() }, null, 2) }] })
);

server.registerTool(
  "moodle_rest_upcoming_deadlines",
  {
    title: "List upcoming Moodle deadlines via REST",
    description: "Uses only the optional environment-configured REST token to read calendar events in the next 90 days. It has no inputs, performs no writes, and is separate from the browser session."
  },
  async () => ({ content: [{ type: "text", text: JSON.stringify({ deadlines: await optionalRestClient().upcomingDeadlines() }, null, 2) }] })
);

(server.registerTool as unknown as (
  name: string,
  config: { title: string; description: string; inputSchema: unknown; annotations: Record<string, boolean> },
  handler: (input: { courseId: number }) => Promise<{ content: Array<{ type: "text"; text: string }> }>
) => unknown)(
  "moodle_rest_course_content",
  {
    title: "Read Moodle course content via REST",
    description: "Reads sections and resource metadata for a numeric course id returned by the optional REST course list. It performs no writes or downloads and is separate from the browser session.",
    inputSchema: { courseId: courseIdSchema },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false }
  },
  async ({ courseId }) => ({ content: [{ type: "text", text: JSON.stringify({ courseId, sections: await optionalRestClient().courseContent(courseId) }, null, 2) }] })
);

(server.registerTool as unknown as (
  name: string,
  config: { title: string; description: string; inputSchema: unknown; annotations: Record<string, boolean> },
  handler: (input: { courseId: number }) => Promise<{ content: Array<{ type: "text"; text: string }> }>
) => unknown)(
  "moodle_rest_course_grades",
  {
    title: "Read my Moodle course grades via REST",
    description: "Reads the current user's grades and feedback for a numeric course id returned by the optional REST course list. It performs no writes and is separate from the browser session.",
    inputSchema: { courseId: courseIdSchema },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false }
  },
  async ({ courseId }) => ({ content: [{ type: "text", text: JSON.stringify({ courseId, grades: await optionalRestClient().courseGrades(courseId) }, null, 2) }] })
);

(server.registerTool as unknown as (
  name: string,
  config: { title: string; description: string; inputSchema: unknown; annotations: Record<string, boolean> },
  handler: (input: { courseId: number }) => Promise<{ content: Array<{ type: "text"; text: string }> }>
) => unknown)(
  "moodle_rest_course_forums",
  {
    title: "Read Moodle course forums via REST",
    description: "Reads forum and announcements metadata for a numeric course id returned by the optional REST course list. It performs no writes and is separate from the browser session.",
    inputSchema: { courseId: courseIdSchema },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false }
  },
  async ({ courseId }) => ({ content: [{ type: "text", text: JSON.stringify({ courseId, forums: await optionalRestClient().courseForums(courseId) }, null, 2) }] })
);

server.registerTool(
  "moodle_browser_login",
  {
    title: "Open the Quinttos UTN Moodle login browser",
    description: "Opens a visible browser at the hard-coded Quinttos UTN Moodle login page. Enter credentials only in that browser; this tool accepts no inputs."
  },
  async () => ({ content: [{ type: "text", text: JSON.stringify(await browserSession.startLogin(), null, 2) }] })
);

server.registerTool(
  "moodle_browser_status",
  {
    title: "Check UTN Moodle browser login status",
    description: "Reports only whether the local visible browser session is waiting for login, authenticated, or closed."
  },
  async () => ({ content: [{ type: "text", text: JSON.stringify(await browserSession.status(), null, 2) }] })
);

server.registerTool(
  "moodle_read_my_profile",
  {
    title: "Read my UTN Moodle profile",
    description: "Reads the signed-in user's visible Moodle profile fields, including any career-related fields rendered by Moodle. It has no inputs and performs no writes."
  },
  async () => ({ content: [{ type: "text", text: JSON.stringify(await browserSession.readMyProfile(), null, 2) }] })
);

server.registerTool(
  "moodle_read_my_courses",
  {
    title: "List my UTN Moodle courses",
    description: "Reads only visible course names and exact-origin URLs from the signed-in user's Moodle courses page. It has no inputs and performs no writes."
  },
  async () => ({ content: [{ type: "text", text: JSON.stringify(await browserSession.readMyCourses(), null, 2) }] })
);

(server.registerTool as unknown as (
  name: string,
  config: { title: string; description: string; inputSchema: unknown; annotations: Record<string, boolean> },
  handler: (input: { course: string }) => Promise<{ content: Array<{ type: "text"; text: string }> }>
) => unknown)(
  "moodle_read_course_activities",
  {
    title: "Read visible activities in my UTN Moodle course",
    description: "Reads visible activity metadata from a course selected by exact title or URL from the signed-in user's visible course list. It performs GET navigation only.",
    inputSchema: { course: z.string().trim().min(1).describe("Exact visible course title or exact visible Moodle course URL") },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false }
  },
  async ({ course }) => ({ content: [{ type: "text", text: JSON.stringify(await browserSession.readCourseActivities(course), null, 2) }] })
);

server.registerTool(
  "moodle_browser_logout",
  {
    title: "Log out and discard the UTN Moodle browser session",
    description: "Requests logout through Moodle's rendered user menu, closes the visible browser, and discards the in-memory session."
  },
  async () => ({ content: [{ type: "text", text: JSON.stringify(await browserSession.logout(), null, 2) }] })
);

async function main(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((error: unknown) => {
  console.error("MCP server failed to start:", error instanceof Error ? error.message : "unknown error");
  process.exitCode = 1;
});
