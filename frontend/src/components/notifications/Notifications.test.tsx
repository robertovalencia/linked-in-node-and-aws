import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, expect, it, vi } from "vitest";
import { AuthProvider, TOKEN_KEY } from "../../contexts/AuthContext";
import { MarketplaceRoute } from "../../routes/MarketplaceRoute";
import { ava, reply } from "../../test/fixtures";
afterEach(() => vi.unstubAllGlobals());
it("restores a session, marks an owned notification read and opens the inquiry workspace", async () => {
  localStorage.setItem(TOKEN_KEY, "saved-token");
  const fetch = vi.fn().mockImplementation((path: string) => {
    if (path === "/api/auth/me")
      return Promise.resolve(
        reply({
          id: "ava",
          name: ava.name,
          email: "ava@demo.local",
          role: "PROVIDER",
        }),
      );
    if (path.startsWith("/api/providers?"))
      return Promise.resolve(reply({ items: [ava], total: 1 }));
    if (path === "/api/notifications")
      return Promise.resolve(
        reply([
          {
            id: "n1",
            inquiryId: "i1",
            message: "Morgan sent a project inquiry",
            read: false,
            createdAt: "2026-10-21T12:00:00Z",
          },
        ]),
      );
    if (path === "/api/notifications/n1/read")
      return Promise.resolve(reply(null, 204));
    if (path === "/api/inquiries") return Promise.resolve(reply([]));
    return Promise.resolve(reply({}, 404));
  });
  vi.stubGlobal("fetch", fetch);
  const user = userEvent.setup();
  render(
    <AuthProvider>
      <MarketplaceRoute />
    </AuthProvider>,
  );
  await user.click(
    await screen.findByRole("button", { name: "Notifications" }),
  );
  const notification = await within(
    screen.getByRole("dialog", { name: "Notifications" }),
  ).findByRole("button", { name: /Morgan sent a project inquiry/ });
  await user.click(notification);
  expect(
    await screen.findByRole("dialog", { name: "Your workspace" }),
  ).toBeVisible();
  expect(fetch).toHaveBeenCalledWith(
    "/api/notifications/n1/read",
    expect.objectContaining({
      method: "PATCH",
      headers: expect.objectContaining({ Authorization: "Bearer saved-token" }),
    }),
  );
});

it("refreshes an initially empty inbox when opened after a new inquiry arrives", async () => {
  localStorage.setItem(TOKEN_KEY, "saved-token");
  let notificationRequests = 0;
  vi.stubGlobal(
    "fetch",
    vi.fn().mockImplementation((path: string) => {
      if (path === "/api/auth/me")
        return Promise.resolve(
          reply({
            id: "ava",
            name: ava.name,
            email: "ava@demo.local",
            role: "PROVIDER",
          }),
        );
      if (path.startsWith("/api/providers?"))
        return Promise.resolve(reply({ items: [ava], total: 1 }));
      if (path === "/api/notifications") {
        notificationRequests++;
        return Promise.resolve(
          reply(
            notificationRequests === 1
              ? []
              : [
                  {
                    id: "new",
                    message: "New project arrived after login",
                    read: false,
                    createdAt: "2026-10-21T12:00:00Z",
                  },
                ],
          ),
        );
      }
      return Promise.resolve(reply({}, 404));
    }),
  );
  const user = userEvent.setup();
  render(
    <AuthProvider>
      <MarketplaceRoute />
    </AuthProvider>,
  );
  const bell = await screen.findByRole("button", { name: "Notifications" });
  await waitFor(() => expect(notificationRequests).toBe(1));
  await user.click(bell);
  expect(
    await screen.findByRole("button", {
      name: /New project arrived after login/,
    }),
  ).toBeVisible();
  expect(notificationRequests).toBe(2);
  expect(screen.queryByText("You’re all caught up")).not.toBeInTheDocument();
});
it("a notification refresh failure is explicit and retry can recover", async () => {
  localStorage.setItem(TOKEN_KEY, "saved-token");
  let notificationRequests = 0;
  vi.stubGlobal(
    "fetch",
    vi.fn().mockImplementation((path: string) => {
      if (path === "/api/auth/me")
        return Promise.resolve(
          reply({
            id: "ava",
            name: ava.name,
            email: "ava@demo.local",
            role: "PROVIDER",
          }),
        );
      if (path.startsWith("/api/providers?"))
        return Promise.resolve(reply({ items: [ava], total: 1 }));
      if (path === "/api/notifications") {
        notificationRequests++;
        return Promise.resolve(
          notificationRequests === 2
            ? reply({ message: "Notification service unavailable" }, 503)
            : reply([]),
        );
      }
      return Promise.resolve(reply({}, 404));
    }),
  );
  const user = userEvent.setup();
  render(
    <AuthProvider>
      <MarketplaceRoute />
    </AuthProvider>,
  );
  const bell = await screen.findByRole("button", { name: "Notifications" });
  await waitFor(() => expect(notificationRequests).toBe(1));
  await user.click(bell);
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Notification service unavailable",
  );
  expect(screen.queryByText("You’re all caught up")).not.toBeInTheDocument();
  await user.click(screen.getByRole("button", { name: "Retry notifications" }));
  expect(await screen.findByText("You’re all caught up")).toBeVisible();
});
