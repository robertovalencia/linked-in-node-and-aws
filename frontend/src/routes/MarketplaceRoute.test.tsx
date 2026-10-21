import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { AuthProvider } from "../contexts/AuthContext";
import { ava, leo, reply } from "../test/fixtures";
import { MarketplaceRoute } from "./MarketplaceRoute";
let requests: { path: string; options?: RequestInit }[];
beforeEach(() => {
  requests = [];
  vi.stubGlobal(
    "fetch",
    vi.fn().mockImplementation((path: string, options?: RequestInit) => {
      requests.push({ path, options });
      if (path.startsWith("/api/providers?"))
        return Promise.resolve(reply({ items: [ava, leo], total: 2 }));
      if (path === "/api/providers/ava") return Promise.resolve(reply(ava));
      if (path === "/api/providers/leo") return Promise.resolve(reply(leo));
      if (path === "/api/auth/login")
        return Promise.resolve(
          reply({
            id: "client",
            email: "company@demo.local",
            name: "Morgan Client",
            role: "CLIENT",
            token: "demo-token",
          }),
        );
      if (path === "/api/notifications") return Promise.resolve(reply([]));
      if (path === "/api/inquiries")
        return Promise.resolve(reply({ id: "inquiry" }, 201));
      return Promise.resolve(reply({ message: "Unexpected route" }, 404));
    }),
  );
  HTMLElement.prototype.scrollIntoView = vi.fn();
});
afterEach(() => vi.unstubAllGlobals());
const mount = () =>
  render(
    <AuthProvider>
      <MarketplaceRoute />
    </AuthProvider>,
  );
describe("marketplace journeys", () => {
  it("searches, filters, compares and opens a full provider profile", async () => {
    const user = userEvent.setup();
    mount();
    await screen.findByRole("button", { name: "Ava Martinez" });
    await user.type(
      screen.getByRole("textbox", { name: "Search services or skills" }),
      "React",
    );
    await user.click(screen.getByRole("button", { name: /Find an expert/ }));
    await waitFor(() =>
      expect(requests.some((r) => r.path.includes("q=React"))).toBe(true),
    );
    await user.click(screen.getByRole("button", { name: /Filters/ }));
    await user.type(
      screen.getByRole("textbox", { name: "Tool or skill" }),
      "Node",
    );
    await waitFor(() =>
      expect(requests.some((r) => r.path.includes("skill=Node"))).toBe(true),
    );
    await user.click(
      screen.getByRole("button", { name: "Add Ava Martinez to comparison" }),
    );
    await user.click(
      screen.getByRole("button", { name: "Add Leo Chen to comparison" }),
    );
    await user.click(screen.getByRole("button", { name: "Compare" }));
    const comparison = await screen.findByRole("dialog", {
      name: "Find your best fit",
    });
    await within(comparison).findByRole("heading", { name: "Ava Martinez" });
    expect(
      within(comparison).getByRole("heading", { name: "Leo Chen" }),
    ).toBeVisible();
    await user.click(
      within(comparison).getAllByRole("button", { name: "View profile" })[0],
    );
    const profile = await screen.findByRole("dialog", {
      name: "Professional profile",
    });
    expect(
      within(profile).getByRole("heading", { name: "Selected work" }),
    ).toBeVisible();
    expect(
      within(profile).getByRole("link", { name: "View project" }),
    ).toHaveAttribute("href", "https://example.com");
  });
  it("continues an anonymous contact through sign-in and submits a private inquiry", async () => {
    const user = userEvent.setup();
    mount();
    await user.click(
      await screen.findByRole("button", { name: "Ava Martinez" }),
    );
    await user.click(
      within(
        screen.getByRole("dialog", { name: "Professional profile" }),
      ).getByRole("button", { name: "Send inquiry" }),
    );
    const login = screen.getByRole("dialog", { name: "Welcome back." });
    await user.click(within(login).getByRole("button", { name: "Sign in" }));
    const inquiry = await screen.findByRole("dialog", {
      name: "Let’s work with Ava",
    });
    await user.type(
      within(inquiry).getByRole("textbox", { name: "Project title" }),
      "Customer portal",
    );
    await user.type(
      within(inquiry).getByRole("textbox", {
        name: "Tell them about your project",
      }),
      "We need a React portal with secure account access.",
    );
    await user.type(
      within(inquiry).getByRole("spinbutton", {
        name: "Estimated budget (USD)",
      }),
      "5000",
    );
    await user.click(
      within(inquiry).getByRole("button", { name: "Send inquiry" }),
    );
    await screen.findByText(
      "Your inquiry was sent. Follow its status in your inbox.",
    );
    const request = requests.find((r) => r.path === "/api/inquiries");
    expect(JSON.parse(request!.options!.body as string)).toMatchObject({
      providerId: "ava",
      budget: 5000,
      subject: "Customer portal",
    });
    expect(request!.options!.headers).toMatchObject({
      Authorization: "Bearer demo-token",
      "Idempotency-Key": expect.any(String),
    });
  });
  it("shows an actionable API failure and recovers on retry", async () => {
    const fetch = vi.mocked(globalThis.fetch);
    fetch.mockResolvedValueOnce(reply({ message: "Catalog unavailable" }, 503));
    const user = userEvent.setup();
    mount();
    expect(await screen.findByText("Catalog unavailable")).toBeVisible();
    await user.click(screen.getByRole("button", { name: "Try again" }));
    expect(
      await screen.findByRole("button", { name: "Ava Martinez" }),
    ).toBeVisible();
  });
});

it("closing a pending contact sign-in prevents delayed auth and canceled inquiry side effects", async () => {
  let finish!: (response: Response) => void;
  const original = globalThis.fetch;
  vi.stubGlobal(
    "fetch",
    vi.fn().mockImplementation((path: string, options?: RequestInit) =>
      path === "/api/auth/login"
        ? new Promise<Response>((resolve) => {
            finish = resolve;
          })
        : original(path, options),
    ),
  );
  const user = userEvent.setup();
  mount();
  await user.click(await screen.findByRole("button", { name: "Ava Martinez" }));
  await user.click(
    within(
      screen.getByRole("dialog", { name: "Professional profile" }),
    ).getByRole("button", { name: "Send inquiry" }),
  );
  const login = screen.getByRole("dialog", { name: "Welcome back." });
  await user.click(within(login).getByRole("button", { name: "Sign in" }));
  await user.click(within(login).getByRole("button", { name: "Close dialog" }));
  finish(
    reply({
      id: "client",
      email: "company@demo.local",
      name: "Morgan",
      role: "CLIENT",
      token: "canceled-token",
    }),
  );
  await waitFor(() =>
    expect(
      screen.queryByRole("dialog", { name: "Welcome back." }),
    ).not.toBeInTheDocument(),
  );
  // Flush the ignored transport completion before checking persistent/auth state.
  await new Promise((resolve) => setTimeout(resolve, 0));
  expect(
    screen.queryByRole("button", { name: "Sign out" }),
  ).not.toBeInTheDocument();
  expect(
    screen.queryByRole("dialog", { name: "Let’s work with Ava" }),
  ).not.toBeInTheDocument();
  expect(localStorage.getItem("expertly-node-aws-token")).toBeNull();
});
