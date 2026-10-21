import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, expect, it, vi } from "vitest";
import { Editor } from "./Editor";
import { Dashboard } from "../inquiries/Dashboard";
import { ava, reply } from "../../test/fixtures";
const auth = {
  id: "ava",
  email: "ava@demo.local",
  name: "Ava Martinez",
  role: "PROVIDER" as const,
  token: "provider-token",
};
afterEach(() => vi.unstubAllGlobals());
it("edits structured provider data and persists a typed profile update", async () => {
  const saved = vi.fn();
  const fetch = vi
    .fn()
    .mockResolvedValueOnce(reply(ava))
    .mockResolvedValueOnce(reply(ava));
  vi.stubGlobal("fetch", fetch);
  const user = userEvent.setup();
  render(<Editor auth={auth} onClose={vi.fn()} onSaved={saved} />);
  const headline = await screen.findByRole("textbox", {
    name: "Professional headline",
  });
  await user.clear(headline);
  await user.type(headline, "NestJS platform engineer");
  await user.click(screen.getByRole("button", { name: "Add project" }));
  const titles = screen.getAllByRole("textbox", { name: "Project title" });
  await user.type(titles[1], "Marketplace");
  const descriptions = screen.getAllByRole("textbox", { name: "Description" });
  await user.type(descriptions[1], "Secure service marketplace");
  const links = screen.getAllByRole("textbox", { name: "Project link" });
  await user.type(links[1], "https://example.com/marketplace");
  await user.click(screen.getByRole("button", { name: "Save profile" }));
  await waitFor(() => expect(saved).toHaveBeenCalledOnce());
  const options = fetch.mock.calls[1][1] as RequestInit;
  expect(JSON.parse(options.body as string)).toMatchObject({
    headline: "NestJS platform engineer",
    portfolio: [
      ava.portfolio[0],
      {
        title: "Marketplace",
        description: "Secure service marketplace",
        url: "https://example.com/marketplace",
      },
    ],
  });
  expect(options.method).toBe("PUT");
});
it("a provider accepts an inquiry and sees the persisted status", async () => {
  const inquiry = {
    id: "i1",
    providerId: ava.id,
    providerName: ava.name,
    clientName: "Morgan",
    subject: "Customer portal",
    message: "Build a customer portal",
    budget: 5000,
    clientType: "COMPANY",
    status: "PENDING",
    createdAt: "2026-10-21T12:00:00Z",
  };
  const fetch = vi
    .fn()
    .mockResolvedValueOnce(reply([inquiry]))
    .mockResolvedValueOnce(reply({ ...inquiry, status: "ACCEPTED" }));
  vi.stubGlobal("fetch", fetch);
  const user = userEvent.setup();
  render(<Dashboard auth={auth} onClose={vi.fn()} onEdit={vi.fn()} />);
  await user.click(
    await screen.findByRole("button", { name: "Accept inquiry" }),
  );
  expect(await screen.findByText("ACCEPTED")).toBeVisible();
  expect(
    screen.queryByRole("button", { name: "Accept inquiry" }),
  ).not.toBeInTheDocument();
  expect(fetch).toHaveBeenLastCalledWith(
    "/api/inquiries/i1/status",
    expect.objectContaining({
      method: "PATCH",
      body: JSON.stringify({ status: "ACCEPTED" }),
    }),
  );
});
it("keeps the workspace usable when a status update fails", async () => {
  const inquiry = {
    id: "i1",
    providerName: "Ava",
    clientName: "Morgan",
    subject: "Customer portal",
    message: "Build a portal",
    budget: 5000,
    clientType: "COMPANY",
    status: "PENDING",
    createdAt: "2026-10-21T12:00:00Z",
  };
  vi.stubGlobal(
    "fetch",
    vi
      .fn()
      .mockResolvedValueOnce(reply([inquiry]))
      .mockResolvedValueOnce(reply({ message: "Update unavailable" }, 503)),
  );
  const user = userEvent.setup();
  render(<Dashboard auth={auth} onClose={vi.fn()} onEdit={vi.fn()} />);
  await user.click(
    await screen.findByRole("button", { name: "Accept inquiry" }),
  );
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Update unavailable",
  );
  expect(
    within(screen.getByRole("dialog")).getByRole("button", {
      name: "Accept inquiry",
    }),
  ).toBeEnabled();
});

it("a failed initial profile load terminates loading and can be retried", async () => {
  vi.stubGlobal(
    "fetch",
    vi
      .fn()
      .mockResolvedValueOnce(reply({ message: "Profile unavailable" }, 503))
      .mockResolvedValueOnce(reply(ava)),
  );
  const user = userEvent.setup();
  render(<Editor auth={auth} onClose={vi.fn()} onSaved={vi.fn()} />);
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Profile unavailable",
  );
  expect(screen.queryByText("Loading…")).not.toBeInTheDocument();
  await user.click(
    screen.getByRole("button", { name: "Retry loading profile" }),
  );
  expect(
    await screen.findByRole("textbox", { name: "Professional headline" }),
  ).toHaveValue(ava.headline);
  expect(screen.queryByRole("alert")).not.toBeInTheDocument();
});
it("a failed initial workspace list does not pretend the inbox is empty and can be retried", async () => {
  vi.stubGlobal(
    "fetch",
    vi
      .fn()
      .mockResolvedValueOnce(reply({ message: "Inbox unavailable" }, 503))
      .mockResolvedValueOnce(reply([])),
  );
  const user = userEvent.setup();
  render(<Dashboard auth={auth} onClose={vi.fn()} onEdit={vi.fn()} />);
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Inbox unavailable",
  );
  expect(
    screen.queryByText("Your next conversation starts here"),
  ).not.toBeInTheDocument();
  expect(screen.queryByText("Loading…")).not.toBeInTheDocument();
  await user.click(
    screen.getByRole("button", { name: "Retry loading inquiries" }),
  );
  expect(
    await screen.findByText("Your next conversation starts here"),
  ).toBeVisible();
  expect(screen.queryByRole("alert")).not.toBeInTheDocument();
});
