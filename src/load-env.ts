import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

/** Load project .env from dist/ or src/ parent, then from process cwd. */
export function loadProjectEnv(): void {
  const candidates = [
    join(dirname(fileURLToPath(import.meta.url)), "..", ".env"),
    join(process.cwd(), ".env")
  ];
  for (const path of candidates) {
    if (!existsSync(path)) continue;
    try {
      process.loadEnvFile(path);
      return;
    } catch {
      // Try the next candidate.
    }
  }
}
