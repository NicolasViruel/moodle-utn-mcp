import { chromium, type Browser, type BrowserContext, type Locator, type Page } from "playwright";
import { QUINTTOS_LOGIN_URL, assertAllowedOrigin } from "./probe.js";

const PROFILE_LINK_SELECTOR = ".usermenu a[href*='/user/profile.php'], #usernavigation a[href*='/user/profile.php'], [data-region='user-menu'] a[href*='/user/profile.php']";
const LOGOUT_LINK_SELECTOR = ".usermenu a[href*='/login/logout.php'], #usernavigation a[href*='/login/logout.php'], [data-region='user-menu'] a[href*='/login/logout.php']";
const USER_MENU_TOGGLE_SELECTOR = ".usermenu .dropdown-toggle, #usernavigation .dropdown-toggle, [data-region='user-menu'] [data-toggle='dropdown']";
const CAMPUS_LINK_TEXT = "Ingresar al Campus Virtual";
const MOODLE_ORIGIN = "https://tup.sied.utn.edu.ar";
const QUINTTOS_ORIGIN = "https://utnsannicolas.quinttos.com";

export type BrowserLoginPhase = "not_started" | "awaiting_login" | "sso_ready" | "authenticated" | "closed";

export interface BrowserLoginStatus {
  phase: BrowserLoginPhase;
  browserVisible: boolean;
  detail: string;
}

interface BrowserSessionDriver {
  launch(options: { headless: boolean }): Promise<Browser>;
}

function isAllowedUrl(value: string): boolean {
  try {
    assertAllowedOrigin(value);
    return true;
  } catch {
    return false;
  }
}

function hasExactOrigin(value: string, origin: string): boolean {
  try {
    return new URL(value).origin === origin;
  } catch {
    return false;
  }
}

export class MoodleBrowserSession {
  private browser?: Browser;
  private context?: BrowserContext;
  private page?: Page;
  private wasStarted = false;

  constructor(private readonly driver: BrowserSessionDriver = chromium) {}

  async startLogin(): Promise<BrowserLoginStatus> {
    if (this.page && !this.page.isClosed()) {
      return this.status();
    }

    this.wasStarted = true;
    this.browser = await this.driver.launch({ headless: false });
    this.context = await this.browser.newContext();
    await this.context.route("**/*", (route) => {
      const requestUrl = route.request().url();
      return isAllowedUrl(requestUrl) ? route.continue() : route.abort();
    });
    this.page = await this.context.newPage();
    await this.page.goto(QUINTTOS_LOGIN_URL, { waitUntil: "domcontentloaded" });
    return this.status();
  }

  async status(): Promise<BrowserLoginStatus> {
    if (!this.page || this.page.isClosed()) {
      return {
        phase: this.wasStarted ? "closed" : "not_started",
        browserVisible: false,
        detail: this.wasStarted ? "The browser session is closed." : "No browser session has been started."
      };
    }

    if (await this.isMoodleSignedIn()) {
      return {
        phase: "authenticated",
        browserVisible: true,
        detail: "Moodle login was detected in the visible UTN browser."
      };
    }

    if (await this.getMoodleCampusLink()) {
      return {
        phase: "sso_ready",
        browserVisible: true,
        detail: "Portal login was detected. Moodle SSO is ready, but Moodle access has not yet been confirmed."
      };
    }

    return {
      phase: "awaiting_login",
      browserVisible: true,
      detail: "Complete login directly in the visible browser, then check status again."
    };
  }

  async readMyProfile(): Promise<{ profile: Record<string, string> }> {
    const page = this.requirePage();
    if (!await this.isMoodleSignedIn() && !await this.continueToMoodleFromPortal()) {
      throw new Error("The visible browser is not authenticated. Complete login directly in Moodle first.");
    }
    if (!await this.isMoodleSignedIn()) {
      throw new Error("Moodle did not confirm authentication after the portal SSO transition.");
    }

    await this.openUserMenu();
    const profileLink = page.locator(PROFILE_LINK_SELECTOR).first();
    if (await profileLink.count() === 0) {
      throw new Error("Moodle did not render an own-profile link in the user menu.");
    }

    await profileLink.click();
    await page.waitForURL((url) => url.origin === MOODLE_ORIGIN && url.pathname === "/user/profile.php");

    const profile = await page.evaluate(() => {
      const content = document.querySelector("main, #region-main, #page-content");
      if (!content) {
        return {};
      }

      const fields: Record<string, string> = {};
      const heading = content.querySelector("h1")?.textContent?.trim();
      if (heading) {
        fields.name = heading;
      }
      for (const label of content.querySelectorAll("dt")) {
        const value = label.nextElementSibling;
        const key = label.textContent?.replace(/\s+/g, " ").trim();
        const text = value?.textContent?.replace(/\s+/g, " ").trim();
        if (key && text) {
          fields[key] = text;
        }
      }
      return fields;
    });

    return { profile };
  }

  async logout(): Promise<{ loggedOut: boolean; detail: string }> {
    const page = this.requirePage();
    let loggedOut = false;
    if (await this.isMoodleSignedIn()) {
      await this.openUserMenu();
      const logoutLink = page.locator(LOGOUT_LINK_SELECTOR).first();
      if (await logoutLink.count() > 0) {
        await logoutLink.click();
        loggedOut = true;
      }
    }
    await this.close();
    return {
      loggedOut,
      detail: loggedOut ? "Moodle logout was requested through its rendered user-menu link and the local browser was closed." : "The local browser was closed and its in-memory session was discarded."
    };
  }

  private requirePage(): Page {
    if (!this.page || this.page.isClosed()) {
      throw new Error("No active visible browser session. Start browser login first.");
    }
    return this.page;
  }

  private async isMoodleSignedIn(): Promise<boolean> {
    const page = this.requirePage();
    return hasExactOrigin(page.url(), MOODLE_ORIGIN)
      && page.evaluate(() => Boolean(document.querySelector("a[href*='/login/logout.php']")));
  }

  private async getMoodleCampusLink(): Promise<Locator | undefined> {
    const page = this.requirePage();
    if (!hasExactOrigin(page.url(), QUINTTOS_ORIGIN)) {
      return undefined;
    }

    const campusLink = page.locator("a").filter({ hasText: new RegExp(`^\\s*${CAMPUS_LINK_TEXT}\\s*$`) }).first();
    const href = await campusLink.getAttribute("href");
    if (!href) {
      return undefined;
    }

    try {
      return new URL(href, page.url()).origin === MOODLE_ORIGIN ? campusLink : undefined;
    } catch {
      return undefined;
    }
  }

  private async continueToMoodleFromPortal(): Promise<boolean> {
    const page = this.requirePage();
    const campusLink = await this.getMoodleCampusLink();
    if (!campusLink) {
      return false;
    }

    await Promise.all([
      page.waitForURL((url) => url.origin === MOODLE_ORIGIN),
      campusLink.click()
    ]);
    return true;
  }

  private async openUserMenu(): Promise<void> {
    const page = this.requirePage();
    const menuToggle = page.locator(USER_MENU_TOGGLE_SELECTOR).first();
    if (await menuToggle.count() > 0) {
      await menuToggle.click();
    }
  }

  private async close(): Promise<void> {
    await this.context?.close();
    this.page = undefined;
    this.context = undefined;
    this.browser = undefined;
  }
}
