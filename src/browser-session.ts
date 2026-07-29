import { chromium, type Browser, type BrowserContext, type Locator, type Page } from "playwright";
import { QUINTTOS_LOGIN_URL, assertAllowedOrigin } from "./probe.js";

const PROFILE_LINK_SELECTOR = ".usermenu a[href*='/user/profile.php'], #usernavigation a[href*='/user/profile.php'], [data-region='user-menu'] a[href*='/user/profile.php']";
const LOGOUT_LINK_SELECTOR = ".usermenu a[href*='/login/logout.php'], #usernavigation a[href*='/login/logout.php'], [data-region='user-menu'] a[href*='/login/logout.php']";
const USER_MENU_TOGGLE_SELECTOR = ".usermenu .dropdown-toggle, #usernavigation .dropdown-toggle, [data-region='user-menu'] [data-toggle='dropdown']";
const CAMPUS_LINK_TEXT = "Ingresar al Campus Virtual";
const MOODLE_ORIGIN = "https://tup.sied.utn.edu.ar";
const QUINTTOS_ORIGIN = "https://utnsannicolas.quinttos.com";
const COURSE_LINK_SELECTOR = "[data-region='course-content'] a[href], .dashboard-card a[href], .course-card a[href], .coursebox .coursename a[href], a.coursename[href]";
const COURSE_READY_SELECTOR = "[data-region='course-content'], .dashboard-card, .course-card, .coursebox, [data-region='no-courses'], [data-region='courses-view'] .alert-info";
const ACTIVITY_SELECTOR = "li.activity, [data-for='cmitem']";

export type BrowserLoginPhase = "not_started" | "awaiting_login" | "sso_ready" | "authenticated" | "closed";

export interface BrowserLoginStatus {
  phase: BrowserLoginPhase;
  browserVisible: boolean;
  detail: string;
}

export interface MoodleCourse {
  name: string;
  url: string;
}

export type MoodleCompletionStatus = "pending" | "completed" | "unknown";

export interface MoodleActivity {
  title: string;
  activityType?: string;
  url?: string;
  completion: MoodleCompletionStatus;
  dueDateText?: string;
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

function completionStatus(value: { text: string; toggleType: string; status: string; state: string; className: string }): MoodleCompletionStatus {
  const marker = `${value.toggleType} ${value.status} ${value.state} ${value.className}`.toLowerCase();
  if (value.state === "1" || value.status === "1" || /mark-undone|completion[_-]complete|\bcomplete(?:d)?\b/.test(marker)) return "completed";
  if (value.state === "0" || value.status === "0" || /mark-done|completion[_-]incomplete|\bincomplete\b/.test(marker)) return "pending";
  const text = value.text.toLowerCase();
  if (/mark as not done|done:|^done$|^completed$|marcar como no completad|^completad[oa]$/.test(text)) return "completed";
  if (/mark as done|to do:|not completed|marcar como completad|por hacer|pendiente/.test(text)) return "pending";
  return "unknown";
}

export class MoodleBrowserSession {
  private browser?: Browser;
  private context?: BrowserContext;
  private page?: Page;
  private wasStarted = false;

  constructor(private readonly driver: BrowserSessionDriver = chromium) {}

  async startLogin(): Promise<BrowserLoginStatus> {
    if (await this.findOpenPage()) {
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
    if (await this.findMoodleSignedInPage()) {
      return {
        phase: "authenticated",
        browserVisible: true,
        detail: "Moodle login was detected in the visible UTN browser."
      };
    }

    const page = await this.findOpenPage();
    if (!page) {
      return {
        phase: this.wasStarted ? "closed" : "not_started",
        browserVisible: false,
        detail: this.wasStarted ? "The browser session is closed." : "No browser session has been started."
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
    let page = await this.findMoodleSignedInPage();
    if (!page && !await this.continueToMoodleFromPortal()) {
      throw new Error("The visible browser is not authenticated. Complete login directly in Moodle first.");
    }
    page = await this.findMoodleSignedInPage();
    if (!page) {
      throw new Error("Moodle did not confirm authentication after the portal SSO transition.");
    }

    await this.openUserMenu(page);
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

  async readMyCourses(): Promise<{ courses: MoodleCourse[] }> {
    let page = await this.findMoodleSignedInPage();
    if (!page && !await this.continueToMoodleFromPortal()) {
      throw new Error("The visible browser is not authenticated. Complete login directly in Moodle first.");
    }
    page = await this.findMoodleSignedInPage();
    if (!page) {
      throw new Error("Moodle did not confirm authentication after the portal SSO transition.");
    }

    return { courses: await this.readVisibleCourses(page) };
  }

  async readCourseActivities(course: string): Promise<{ course: MoodleCourse; activities: MoodleActivity[] }> {
    const selector = course.trim();
    if (!selector) throw new Error("A visible course title or exact course URL is required.");
    if (selector.includes("://")) {
      let requested: URL;
      try { requested = new URL(selector); } catch { throw new Error("The course URL is invalid."); }
      if (requested.origin !== MOODLE_ORIGIN || requested.pathname !== "/course/view.php") {
        throw new Error("Course URLs must use the exact Moodle origin and /course/view.php path.");
      }
    }

    let page = await this.findMoodleSignedInPage();
    if (!page && !await this.continueToMoodleFromPortal()) throw new Error("The visible browser is not authenticated. Complete login directly in Moodle first.");
    page = await this.findMoodleSignedInPage();
    if (!page) throw new Error("Moodle did not confirm authentication after the portal SSO transition.");

    const courses = await this.readVisibleCourses(page);
    const matches = courses.filter((item) => item.name === selector || item.url === selector);
    if (matches.length !== 1) throw new Error(matches.length ? "The course title is ambiguous; use its exact visible URL." : "The requested course is not in the visible course list.");
    const selected = matches[0];
    await page.goto(selected.url, { waitUntil: "domcontentloaded" });
    if (!hasExactOrigin(page.url(), MOODLE_ORIGIN) || new URL(page.url()).pathname !== "/course/view.php") {
      throw new Error("Moodle did not load the selected visible course.");
    }

    const rawActivities = await page.evaluate((activitySelector) => Array.from(document.querySelectorAll<HTMLElement>(activitySelector))
      .filter((row, index, rows) => !rows.some((parent, parentIndex) => parentIndex !== index && parent.contains(row)))
      .filter((row) => {
        const style = window.getComputedStyle(row);
        return !row.closest("[hidden], [aria-hidden='true']") && style.display !== "none" && style.visibility !== "hidden";
      })
      .map((row) => {
        const visibleText = (element: Element | null) => {
          if (!element) return "";
          const copy = element.cloneNode(true) as Element;
          copy.querySelectorAll(".accesshide, .sr-only, .visually-hidden").forEach((hidden) => hidden.remove());
          return copy.textContent?.replace(/\s+/g, " ").trim() ?? "";
        };
        const link = row.querySelector<HTMLAnchorElement>(".activityname a[href], a.aalink[href*='/mod/'], a[href*='/mod/']");
        const title = row.dataset.activityname || visibleText(row.querySelector(".instancename, .activityname")) || visibleText(link);
        const completion = row.querySelector<HTMLElement>("[data-toggletype], [data-completionstatus], [data-completionstate], [data-region='completion-info'], .completion-info, .completionstatus");
        const dateText = Array.from(row.querySelectorAll(".activity-dates, [data-region='activity-dates'], .availabilityinfo, [data-region='availability-info']"))
          .map((element) => visibleText(element)).find((text) => /\b(due|closes?|deadline|fecha de entrega|vence|cierra)\b/i.test(text));
        const href = link?.getAttribute("href") ?? "";
        const pathType = href.match(/\/mod\/([^/]+)\/view\.php/i)?.[1];
        return { title, href, activityType: row.dataset.modname || row.className.match(/\bmodtype_([\w-]+)/)?.[1] || pathType || "", dueDateText: dateText,
          completion: { text: visibleText(completion), toggleType: completion?.dataset.toggletype ?? "", status: completion?.dataset.completionstatus ?? "", state: completion?.dataset.completionstate ?? "", className: completion?.className ?? "" } };
      }), ACTIVITY_SELECTOR);

    const activities = new Map<string, MoodleActivity>();
    for (const raw of rawActivities) {
      if (!raw.title) continue;
      let url: string | undefined;
      try {
        const candidate = new URL(raw.href, MOODLE_ORIGIN);
        if (candidate.origin === MOODLE_ORIGIN && /^\/mod\/[^/]+\/view\.php$/.test(candidate.pathname)) url = candidate.href;
      } catch { /* Ignore malformed rendered links. */ }
      const activity: MoodleActivity = { title: raw.title, activityType: raw.activityType || undefined, url, completion: completionStatus(raw.completion), dueDateText: raw.dueDateText || undefined };
      const key = url ?? `${activity.activityType ?? ""}\u0000${activity.title}`;
      const existing = activities.get(key);
      if (!existing) activities.set(key, activity);
      else {
        existing.activityType ??= activity.activityType;
        existing.url ??= activity.url;
        existing.dueDateText ??= activity.dueDateText;
        if (existing.completion === "unknown") existing.completion = activity.completion;
      }
    }
    return { course: selected, activities: [...activities.values()] };
  }

  async logout(): Promise<{ loggedOut: boolean; detail: string }> {
    const page = await this.findMoodleSignedInPage();
    let loggedOut = false;
    if (page) {
      await this.openUserMenu(page);
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

  private async isMoodleSignedIn(page: Page): Promise<boolean> {
    return hasExactOrigin(page.url(), MOODLE_ORIGIN)
      && page.evaluate(() => Boolean(document.querySelector("a[href*='/login/logout.php']")));
  }

  // Moodle SSO can complete in a new tab or popup within the same isolated context.
  private async findMoodleSignedInPage(): Promise<Page | undefined> {
    for (const page of this.context?.pages() ?? []) {
      if (!page.isClosed() && await this.isMoodleSignedIn(page)) {
        this.page = page;
        return page;
      }
    }
    return undefined;
  }

  private async findOpenPage(): Promise<Page | undefined> {
    if (this.page && !this.page.isClosed()) {
      return this.page;
    }
    const page = this.context?.pages().find((candidate) => !candidate.isClosed());
    if (page) {
      this.page = page;
    }
    return page;
  }

  private async readVisibleCourses(page: Page): Promise<MoodleCourse[]> {
    await page.goto(`${MOODLE_ORIGIN}/my/courses.php`, { waitUntil: "domcontentloaded" });
    if (!hasExactOrigin(page.url(), MOODLE_ORIGIN) || new URL(page.url()).pathname !== "/my/courses.php") {
      throw new Error("Moodle did not load the signed-in user's courses page.");
    }
    try {
      await page.waitForFunction((selector) => Boolean(document.querySelector(selector)), COURSE_READY_SELECTOR, { timeout: 10_000 });
    } catch {
      throw new Error("Moodle did not finish rendering the visible course list.");
    }
    const links = await page.evaluate((selector) => Array.from(document.querySelectorAll<HTMLAnchorElement>(selector)).filter((anchor) => {
      const style = window.getComputedStyle(anchor);
      return !anchor.closest("[hidden], [aria-hidden='true']") && style.display !== "none" && style.visibility !== "hidden";
    }).map((anchor) => {
      const card = anchor.closest("[data-region='course-content'], .dashboard-card, .course-card, .coursebox");
      const label = anchor.querySelector(".multiline, [data-region='course-name']") ?? card?.querySelector(".coursename, .multiline, [data-region='course-name']");
      return { name: (label?.textContent ?? anchor.getAttribute("aria-label") ?? anchor.textContent ?? "").replace(/\s+/g, " ").trim(), href: anchor.getAttribute("href") ?? "" };
    }), COURSE_LINK_SELECTOR);
    const courses = new Map<string, MoodleCourse>();
    for (const { name, href } of links) {
      if (!name) continue;
      try {
        const url = new URL(href, MOODLE_ORIGIN);
        if (url.origin === MOODLE_ORIGIN && url.pathname === "/course/view.php" && !courses.has(url.href)) courses.set(url.href, { name, url: url.href });
      } catch { /* Ignore malformed rendered links. */ }
    }
    return [...courses.values()];
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

    await campusLink.click();
    return Boolean(await this.findMoodleSignedInPage());
  }

  private async openUserMenu(page: Page): Promise<void> {
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
