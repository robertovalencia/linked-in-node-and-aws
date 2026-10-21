import type {
  Auth,
  Inquiry,
  Notification,
  Provider,
} from "../types/marketplace";
import { api } from "./http";
export const identityService = {
  me: (token: string, signal?: AbortSignal) =>
    api<Omit<Auth, "token">>("/api/auth/me", { token } as Auth, { signal }),
  login: (email: string, password: string, signal?: AbortSignal) =>
    api<Auth>("/api/auth/login", null, {
      method: "POST",
      body: JSON.stringify({ email, password }),
      signal,
    }),
};
export const providerService = {
  list: (params: URLSearchParams, signal?: AbortSignal) =>
    api<{ items: Provider[]; total: number }>(
      `/api/providers?${params}`,
      null,
      { signal },
    ),
  get: (id: string, signal?: AbortSignal) =>
    api<Provider>(`/api/providers/${encodeURIComponent(id)}`, null, { signal }),
  mine: (auth: Auth, signal?: AbortSignal) =>
    api<Provider>("/api/providers/me", auth, { signal }),
  update: (auth: Auth, profile: Provider) =>
    api<Provider>("/api/providers/me", auth, {
      method: "PUT",
      body: JSON.stringify(profile),
    }),
};
export type CreateInquiry = Pick<
  Inquiry,
  "providerId" | "subject" | "message" | "budget" | "clientType"
>;
export const inquiryService = {
  list: (auth: Auth, signal?: AbortSignal) =>
    api<Inquiry[]>("/api/inquiries", auth, { signal }),
  create: (auth: Auth, key: string, data: CreateInquiry) =>
    api<Inquiry>("/api/inquiries", auth, {
      method: "POST",
      headers: { "Idempotency-Key": key },
      body: JSON.stringify(data),
    }),
  respond: (auth: Auth, id: string, status: string) =>
    api<Inquiry>(`/api/inquiries/${encodeURIComponent(id)}/status`, auth, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    }),
};
export const notificationService = {
  list: (auth: Auth, signal?: AbortSignal) =>
    api<Notification[]>("/api/notifications", auth, { signal }),
  read: (auth: Auth, id: string) =>
    api<void>(`/api/notifications/${encodeURIComponent(id)}/read`, auth, {
      method: "PATCH",
    }),
};
