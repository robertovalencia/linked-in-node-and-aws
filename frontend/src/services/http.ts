import type { Auth } from "../types/marketplace";
export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}
export async function api<T>(
  path: string,
  auth: Auth | null = null,
  options: RequestInit = {},
): Promise<T> {
  const res = await fetch(path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(auth ? { Authorization: `Bearer ${auth.token}` } : {}),
      ...options.headers,
    },
  });
  if (!res.ok) {
    let detail = "The request could not be completed.";
    try {
      const e = await res.json();
      detail =
        e.detail ||
        (Array.isArray(e.message) ? e.message.join("; ") : e.message) ||
        detail;
    } catch {}
    throw new ApiError(
      res.status === 401
        ? "Your session has expired. Please sign in again."
        : detail,
      res.status,
    );
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}
