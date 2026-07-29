# moodle-utn-mcp

Local stdio MCP server for the approved UTN Moodle origins `https://tup.sied.utn.edu.ar` and `https://utnsannicolas.quinttos.com`. It offers a user-operated, visible-browser login at the Quinttos login page and read-only tools for the signed-in user's own rendered Moodle profile, courses, and course activities.

## Scope and safety

- The only targets are the hard-coded `https://tup.sied.utn.edu.ar` and `https://utnsannicolas.quinttos.com` origins. The activity tool accepts a course title or URL, but navigates only to an exact course URL freshly discovered in the visible course list. The browser context blocks every request to another origin.
- `moodle_browser_login` launches a visible Chromium window at `https://utnsannicolas.quinttos.com/index.php/login`. The user enters credentials directly in the site; no MCP tool has credential inputs.
- The browser context, cookies, and session state exist only in process memory. No storage state, cookies, tokens, screenshots, or credentials are written to disk, logs, stdout, configuration, or source.
- The implementation does not request Moodle REST tokens, call REST web-service endpoints, use QR codes, automate login fields, or expose session data.
- Authenticated reads are limited to `moodle_read_my_profile`, `moodle_read_my_courses`, and `moodle_read_course_activities`. Course activity reads return only visible title, type/link when available, explicit completion state, and due-date text.
- There are no write, enrollment, coursework, or submission actions. `moodle_browser_logout` is the sole state-changing operation and explicitly ends the local session.
- Diagnostic URLs remove query strings.

The browser session is intentionally local and ephemeral. Restarting the MCP always requires a new user-operated login.

## Requirements

- Node.js 20 or newer
- Playwright Chromium. Install it after dependencies:

```powershell
npx playwright install chromium
```

## Install and verify

```bash
npm install
npx playwright install chromium
npm test
npm run smoke
```

`npm run smoke` makes the unauthenticated public probe and prints a JSON report. It does not attempt login or send credentials.

## Run as an MCP server

```bash
npm start
```

The server uses stdio, so stdout is reserved for MCP JSON-RPC. Configure a client later with the command `node` and argument `dist/index.js` after building. No global OpenCode configuration is modified by this project.

## Tool

### `moodle_probe_capabilities`

Has no inputs. It reports:

- Public Moodle identity and version hints, only when present in the root response.
- Reachability of `/login/index.php`.
- A reminder to use the local browser-login flow.

### `moodle_browser_login`

Has no inputs. Opens a visible browser only at the hard-coded Quinttos UTN Moodle login page. Complete login in that window, then call `moodle_browser_status`.

### `moodle_browser_status`

Has no inputs. Returns `not_started`, `awaiting_login`, `sso_ready`, `authenticated`, or `closed`. It scans every page in the same isolated browser context, so Moodle authentication completed in an SSO-created tab or popup is used. `sso_ready` means Quinttos rendered its Campus link with the exact Moodle origin and the tool can attempt the SSO transition; it does not claim Moodle access. `authenticated` means Moodle's rendered authenticated UI was confirmed. It never returns cookies, URLs with query strings, tokens, or credentials.

### `moodle_read_my_profile`

Has no inputs. From `sso_ready`, it follows only Quinttos's rendered Campus link when its resolved origin is exactly Moodle, then requires Moodle's authenticated UI. It opens the signed-in user's profile using Moodle's rendered user-menu link and returns only visible profile fields. Career information is included only when Moodle displays it in that profile.

### `moodle_read_my_courses`

Has no inputs. It scans the isolated browser context for an authenticated Moodle page, then loads only Moodle's fixed `/my/courses.php` page and waits for its dynamic course cards. It returns deduplicated visible course names and exact-origin `/course/view.php` URLs.

### `moodle_read_course_activities`

Accepts `{ "course": "<exact visible title or exact visible course URL>" }`. It refreshes the visible course list, enters only the unique matching course, and returns `{ course, activities }`. Each activity contains `title`, `completion` (`pending`, `completed`, or `unknown`), and available `activityType`, `url`, and `dueDateText` fields.

### `moodle_browser_logout`

Has no inputs. Uses Moodle's rendered logout link when present, closes the visible browser, and discards the in-memory context. Use it whenever profile access is no longer needed.

## Dependencies

- `@modelcontextprotocol/sdk` 1.29.0: official TypeScript MCP SDK.
- `playwright` 1.58.2: local visible Chromium browser automation and origin request enforcement.
- `zod` 3.24.2: MCP SDK peer dependency.
- `typescript` 5.8.3 and `@types/node` 22.15.3: build-time dependencies.
