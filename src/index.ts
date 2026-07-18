import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { probeCapabilities } from "./probe.js";
import { MoodleBrowserSession } from "./browser-session.js";

const server = new McpServer({
  name: "moodle-utn-mcp",
  version: "0.1.0"
});
const browserSession = new MoodleBrowserSession();

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
