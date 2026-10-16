import { ApiError } from "../services/api";

export function formatError(err: unknown): string {
  if (err instanceof ApiError) {
    return JSON.stringify({ detail: err.detail });
  }
  if (err instanceof Error) {
    return JSON.stringify({ detail: err.message });
  }
  return JSON.stringify({ detail: "Error desconocido" });
}
