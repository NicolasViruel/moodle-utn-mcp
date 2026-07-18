import assert from "node:assert/strict";
import test from "node:test";
import type { Browser, BrowserContext, Locator, Page } from "playwright";
import { MoodleBrowserSession } from "../browser-session.js";

interface FixtureOptions {
  campusHref?: string;
  currentUrl?: string;
  moodleAuthenticated?: boolean;
  ssoProducesMoodleAuthentication?: boolean;
}

function createSession(options: FixtureOptions = {}) {
  const requests: string[] = [];
  let routeHandler: ((route: { request(): { url(): string }; continue(): Promise<void>; abort(): Promise<void> }) => Promise<void>) | undefined;
  let campusClicks = 0;
  let profileClicks = 0;
  let logoutClicks = 0;
  let closed = false;
  let currentUrl = options.currentUrl ?? "https://utnsannicolas.quinttos.com/dashboard";
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
    goto: async (url: string) => { requests.push(url); },
    waitForURL: async (predicate: (url: URL) => boolean) => {
      await Promise.resolve();
      assert.equal(predicate(new URL(currentUrl)), true);
    },
    evaluate: async (callback: () => unknown) => callback.toString().includes("logout")
      ? moodleAuthenticated
      : { name: "Student Name", Carrera: "TUP" },
    locator: (selector: string) => {
      if (selector === "a") {
        return { filter: () => campusLocator };
      }
      return selector.includes("dropdown-toggle") ? menuLocator : selector.includes("logout") ? logoutLocator : profileLocator;
    }
  } as unknown as Page;
  const context = {
    route: async (_pattern: string, handler: typeof routeHandler) => { routeHandler = handler; },
    newPage: async () => page,
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

test("logs out through the rendered Moodle UI and closes the in-memory browser context", async () => {
  const fixture = createSession({ currentUrl: "https://tup.sied.utn.edu.ar/", moodleAuthenticated: true });
  await fixture.session.startLogin();
  const result = await fixture.session.logout();
  assert.equal(fixture.getLogoutClicks(), 1);
  assert.equal(result.loggedOut, true);
  assert.equal(fixture.isClosed(), true);
  assert.equal((await fixture.session.status()).phase, "closed");
});
