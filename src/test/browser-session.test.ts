import assert from "node:assert/strict";
import test from "node:test";
import type { Browser, BrowserContext, Locator, Page } from "playwright";
import { MoodleBrowserSession } from "../browser-session.js";

interface FixtureOptions {
  campusHref?: string;
  currentUrl?: string;
  moodleAuthenticated?: boolean;
  moodlePopupAuthenticated?: boolean;
  ssoProducesMoodleAuthentication?: boolean;
  courseLinks?: Array<{ name: string; href: string; variant?: "current" | "legacy" }>;
  activityRows?: Array<{ title: string; href: string; activityType: string; dueDateText?: string; completion: { text: string; toggleType: string; status: string; state: string; className: string } }>;
}

function createSession(options: FixtureOptions = {}) {
  const requests: string[] = [];
  let routeHandler: ((route: { request(): { url(): string }; continue(): Promise<void>; abort(): Promise<void> }) => Promise<void>) | undefined;
  let campusClicks = 0;
  let profileClicks = 0;
  let logoutClicks = 0;
  let courseReadyWaits = 0;
  let closed = false;
  let currentUrl = options.currentUrl ?? "https://utnsannicolas.quinttos.com/dashboard";
  let popupCurrentUrl = "https://tup.sied.utn.edu.ar/my/courses.php";
  let moodleAuthenticated = options.moodleAuthenticated ?? false;

  const campusLocator = {
    first: () => campusLocator,
    count: async () => options.campusHref ? 1 : 0,
    getAttribute: async (name: string) => name === "href" ? options.campusHref ?? null : null,
    click: async () => {
      campusClicks += 1;
      currentUrl = options.campusHref ?? currentUrl;
      moodleAuthenticated = options.ssoProducesMoodleAuthentication ?? true;
    }
  } as unknown as Locator;
  const profileLocator = {
    first: () => profileLocator,
    count: async () => 1,
    click: async () => {
      profileClicks += 1;
      currentUrl = "https://tup.sied.utn.edu.ar/user/profile.php?id=1";
    }
  } as unknown as Locator;
  const logoutLocator = {
    first: () => logoutLocator,
    count: async () => 1,
    click: async () => { logoutClicks += 1; }
  } as unknown as Locator;
  const menuLocator = {
    first: () => menuLocator,
    count: async () => 0,
    click: async () => { throw new Error("The menu toggle should not be clicked by this fixture."); }
  } as unknown as Locator;
  const page = {
    isClosed: () => false,
    url: () => currentUrl,
    goto: async (url: string) => {
      requests.push(url);
      if (url.startsWith("https://tup.sied.utn.edu.ar/")) currentUrl = url;
    },
    waitForFunction: async () => { courseReadyWaits += 1; return true; },
    waitForURL: async (predicate: (url: URL) => boolean) => {
      await Promise.resolve();
      assert.equal(predicate(new URL(currentUrl)), true);
    },
    evaluate: async (callback: () => unknown, selector?: string) => callback.toString().includes("logout")
      ? moodleAuthenticated
      : selector?.includes("course-content")
        ? (options.courseLinks ?? []).filter(({ variant }) => !variant || selector.includes(variant === "current" ? "course-content" : "coursebox"))
        : selector?.includes("cmitem") ? options.activityRows ?? [] : { name: "Student Name", Carrera: "TUP" },
    locator: (selector: string) => {
      if (selector === "a") {
        return { filter: () => campusLocator };
      }
      return selector.includes("dropdown-toggle") ? menuLocator : selector.includes("logout") ? logoutLocator : profileLocator;
    }
  } as unknown as Page;
  const popupProfileLocator = {
    first: () => popupProfileLocator,
    count: async () => 1,
    click: async () => {
      profileClicks += 1;
      popupCurrentUrl = "https://tup.sied.utn.edu.ar/user/profile.php?id=1";
    }
  } as unknown as Locator;
  const popupPage = {
    isClosed: () => false,
    url: () => popupCurrentUrl,
    goto: async (url: string) => {
      requests.push(url);
      popupCurrentUrl = url;
    },
    waitForFunction: async () => { courseReadyWaits += 1; return true; },
    waitForURL: async (predicate: (url: URL) => boolean) => {
      await Promise.resolve();
      assert.equal(predicate(new URL(popupCurrentUrl)), true);
    },
    evaluate: async (callback: () => unknown, selector?: string) => callback.toString().includes("logout")
      ? options.moodlePopupAuthenticated
      : selector?.includes("course-content")
        ? (options.courseLinks ?? []).filter(({ variant }) => !variant || selector.includes(variant === "current" ? "course-content" : "coursebox"))
        : selector?.includes("cmitem") ? options.activityRows ?? [] : { name: "Student Name", Carrera: "TUP" },
    locator: (selector: string) => selector.includes("dropdown-toggle") ? menuLocator : selector.includes("logout") ? logoutLocator : popupProfileLocator
  } as unknown as Page;
  const context = {
    route: async (_pattern: string, handler: typeof routeHandler) => { routeHandler = handler; },
    newPage: async () => page,
    pages: () => options.moodlePopupAuthenticated ? [page, popupPage] : [page],
    close: async () => { closed = true; }
  } as unknown as BrowserContext;
  const browser = { newContext: async () => context } as unknown as Browser;
  const driver = { launch: async (launchOptions: { headless: boolean }) => {
    assert.equal(launchOptions.headless, false);
    return browser;
  } };

  return {
    session: new MoodleBrowserSession(driver),
    requests,
    getRouteHandler: () => routeHandler,
    getCampusClicks: () => campusClicks,
    getProfileClicks: () => profileClicks,
    getLogoutClicks: () => logoutClicks,
    getCourseReadyWaits: () => courseReadyWaits,
    isClosed: () => closed
  };
}

test("opens Quinttos and allows only the two hard-coded origins", async () => {
  const fixture = createSession();
  const status = await fixture.session.startLogin();
  assert.equal(status.phase, "awaiting_login");
  assert.deepEqual(fixture.requests, ["https://utnsannicolas.quinttos.com/index.php/login"]);

  const handler = fixture.getRouteHandler();
  assert.ok(handler);
  let allowed = false;
  await handler({ request: () => ({ url: () => "https://tup.sied.utn.edu.ar/theme/image.png" }), continue: async () => { allowed = true; }, abort: async () => {} });
  assert.equal(allowed, true);
  let quinttosAllowed = false;
  await handler({ request: () => ({ url: () => "https://utnsannicolas.quinttos.com/theme/image.png" }), continue: async () => { quinttosAllowed = true; }, abort: async () => {} });
  assert.equal(quinttosAllowed, true);
  let blocked = false;
  await handler({ request: () => ({ url: () => "https://example.com/tracker.js" }), continue: async () => {}, abort: async () => { blocked = true; } });
  assert.equal(blocked, true);
});

test("reports the authenticated Quinttos dashboard as SSO-ready without claiming Moodle access", async () => {
  const fixture = createSession({ campusHref: "https://tup.sied.utn.edu.ar/" });
  await fixture.session.startLogin();

  const status = await fixture.session.status();
  assert.equal(status.phase, "sso_ready");
  assert.match(status.detail, /Moodle access has not yet been confirmed/);
});

test("discovers authenticated Moodle in an SSO-created tab before status and profile actions", async () => {
  const fixture = createSession({ moodlePopupAuthenticated: true });
  await fixture.session.startLogin();

  assert.equal((await fixture.session.status()).phase, "authenticated");
  const result = await fixture.session.readMyProfile();
  assert.equal(fixture.getProfileClicks(), 1);
  assert.deepEqual(result, { profile: { name: "Student Name", Carrera: "TUP" } });
});

test("follows only the exact Moodle-origin rendered Campus link before reading the profile", async () => {
  const fixture = createSession({ campusHref: "https://tup.sied.utn.edu.ar/" });
  await fixture.session.startLogin();

  const result = await fixture.session.readMyProfile();
  assert.equal(fixture.getCampusClicks(), 1);
  assert.equal(fixture.getProfileClicks(), 1);
  assert.deepEqual(result, { profile: { name: "Student Name", Carrera: "TUP" } });
});

test("does not trust or follow a rendered Campus link outside the exact Moodle origin", async () => {
  const fixture = createSession({ campusHref: "https://example.com/moodle" });
  await fixture.session.startLogin();

  assert.equal((await fixture.session.status()).phase, "awaiting_login");
  await assert.rejects(fixture.session.readMyProfile(), /not authenticated/);
  assert.equal(fixture.getCampusClicks(), 0);
});

test("keeps Moodle without authenticated UI awaiting login", async () => {
  const fixture = createSession({ currentUrl: "https://tup.sied.utn.edu.ar/", moodleAuthenticated: false });
  const status = await fixture.session.startLogin();

  assert.equal(status.phase, "awaiting_login");
});

test("waits for current and legacy course links, then filters and deduplicates them", async () => {
  const fixture = createSession({
    currentUrl: "https://tup.sied.utn.edu.ar/",
    moodleAuthenticated: true,
    courseLinks: [
      { name: "Algorithms", href: "/course/view.php?id=42", variant: "current" },
      { name: "Algorithms", href: "https://tup.sied.utn.edu.ar/course/view.php?id=42" },
      { name: "Legacy course", href: "/course/view.php?id=7", variant: "legacy" },
      { name: "External course", href: "https://example.com/course/view.php?id=1" },
      { name: "Not a course", href: "/user/profile.php?id=1" }
    ]
  });
  await fixture.session.startLogin();

  const result = await fixture.session.readMyCourses();
  assert.deepEqual(result, {
    courses: [
      { name: "Algorithms", url: "https://tup.sied.utn.edu.ar/course/view.php?id=42" },
      { name: "Legacy course", url: "https://tup.sied.utn.edu.ar/course/view.php?id=7" }
    ]
  });
  assert.equal(fixture.getCourseReadyWaits(), 1);
  assert.ok(fixture.requests.includes("https://tup.sied.utn.edu.ar/my/courses.php"));
});

test("rejects non-course and non-Moodle selectors without navigating to them", async () => {
  for (const selector of ["https://example.com/course/view.php?id=1", "https://tup.sied.utn.edu.ar/user/profile.php?id=1"]) {
    const fixture = createSession({ currentUrl: "https://tup.sied.utn.edu.ar/", moodleAuthenticated: true });
    await fixture.session.startLogin();
    await assert.rejects(fixture.session.readCourseActivities(selector), /exact Moodle origin and \/course\/view\.php path/);
    assert.equal(fixture.requests.includes(selector), false);
  }
});

test("rejects a course that is not in the freshly read visible list", async () => {
  const fixture = createSession({ currentUrl: "https://tup.sied.utn.edu.ar/", moodleAuthenticated: true, courseLinks: [{ name: "Algorithms", href: "/course/view.php?id=42" }] });
  await fixture.session.startLogin();
  await assert.rejects(fixture.session.readCourseActivities("Databases"), /not in the visible course list/);
  assert.deepEqual(fixture.requests.slice(-1), ["https://tup.sied.utn.edu.ar/my/courses.php"]);
});

test("reads deduplicated visible activities with conservative completion and due-date metadata", async () => {
  const unknown = { text: "", toggleType: "", status: "", state: "", className: "" };
  const fixture = createSession({ currentUrl: "https://tup.sied.utn.edu.ar/", moodleAuthenticated: true,
    courseLinks: [{ name: "Algorithms", href: "/course/view.php?id=42" }], activityRows: [
      { title: "Exercise 1", href: "/mod/assign/view.php?id=3", activityType: "assign", dueDateText: "Due: Friday", completion: { ...unknown, toggleType: "manual:mark-done" } },
      { title: "Exercise 1", href: "/mod/assign/view.php?id=3", activityType: "assign", completion: unknown },
      { title: "Quiz", href: "/mod/quiz/view.php?id=4", activityType: "quiz", completion: { ...unknown, state: "1" } },
      { title: "Reading", href: "https://example.com/mod/page/view.php?id=5", activityType: "page", completion: unknown }
    ] });
  await fixture.session.startLogin();
  const result = await fixture.session.readCourseActivities("Algorithms");
  assert.deepEqual(result.activities.map(({ title, completion }) => ({ title, completion })), [
    { title: "Exercise 1", completion: "pending" }, { title: "Quiz", completion: "completed" }, { title: "Reading", completion: "unknown" }
  ]);
  assert.equal(result.activities[0].dueDateText, "Due: Friday");
  assert.equal(result.activities[2].url, undefined);
  assert.equal(fixture.requests.every((url) => new URL(url).origin !== "https://example.com"), true);
});

test("logs out through the rendered Moodle UI and closes the in-memory browser context", async () => {
  const fixture = createSession({ currentUrl: "https://tup.sied.utn.edu.ar/", moodleAuthenticated: true });
  await fixture.session.startLogin();
  const result = await fixture.session.logout();
  assert.equal(fixture.getLogoutClicks(), 1);
  assert.equal(result.loggedOut, true);
  assert.equal(fixture.isClosed(), true);
  assert.equal((await fixture.session.status()).phase, "closed");
});
