import { act, renderHook, waitFor } from "@testing-library/react";
import type { PropsWithChildren } from "react";
import { afterEach, expect, it, vi } from "vitest";
import { AuthProvider, TOKEN_KEY } from "./AuthContext";
import { useAuth } from "../hooks/useAuth";
import { reply } from "../test/fixtures";
const wrapper = ({ children }: PropsWithChildren) => (
  <AuthProvider>{children}</AuthProvider>
);
afterEach(() => vi.unstubAllGlobals());
it("restores server-validated identity and removes expired tokens", async () => {
  localStorage.setItem(TOKEN_KEY, "expired");
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(reply({}, 401)));
  const { result } = renderHook(useAuth, { wrapper });
  await waitFor(() => expect(result.current.restoring).toBe(false));
  expect(result.current.auth).toBeNull();
  expect(localStorage.getItem(TOKEN_KEY)).toBeNull();
});
it("a slow session restore cannot overwrite a newer login", async () => {
  let finish!: (response: Response) => void;
  localStorage.setItem(TOKEN_KEY, "old-token");
  vi.stubGlobal(
    "fetch",
    vi.fn().mockImplementation(
      () =>
        new Promise<Response>((resolve) => {
          finish = resolve;
        }),
    ),
  );
  const { result } = renderHook(useAuth, { wrapper });
  const newer = {
    id: "new",
    token: "new-token",
    name: "New User",
    email: "new@example.com",
    role: "CLIENT" as const,
  };
  act(() => result.current.setAuth(newer));
  await act(async () => {
    finish(
      reply({
        id: "old",
        name: "Old User",
        email: "old@example.com",
        role: "CLIENT",
      }),
    );
  });
  expect(result.current.auth).toEqual(newer);
  expect(localStorage.getItem(TOKEN_KEY)).toBe("new-token");
});
