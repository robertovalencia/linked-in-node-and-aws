import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, expect, it, vi } from "vitest";
import { InquiryForm } from "./InquiryForm";
import { ava, reply } from "../../test/fixtures";
const auth = {
  token: "client-token",
  id: "client",
  email: "company@demo.local",
  name: "Morgan",
  role: "CLIENT" as const,
};
const payload = {
  providerId: ava.id,
  subject: "Customer portal",
  message: "Build a secure portal for our customer accounts.",
  budget: 5000,
  clientType: "COMPANY",
};
afterEach(() => vi.unstubAllGlobals());
async function fill(user: ReturnType<typeof userEvent.setup>) {
  await user.type(
    screen.getByRole("textbox", { name: "Project title" }),
    payload.subject,
  );
  await user.type(
    screen.getByRole("textbox", { name: "Tell them about your project" }),
    payload.message,
  );
  await user.type(
    screen.getByRole("spinbutton", { name: "Estimated budget (USD)" }),
    String(payload.budget),
  );
}
it("freezes a lost-success attempt across close/reopen and retries the exact canonical body/key", async () => {
  const fetch = vi
    .fn()
    .mockRejectedValueOnce(new TypeError("Response was lost after commit"))
    .mockResolvedValueOnce(reply({ ...payload, id: "i1" }, 201));
  vi.stubGlobal("fetch", fetch);
  const user = userEvent.setup();
  const sent = vi.fn();
  const first = render(
    <InquiryForm auth={auth} provider={ava} onClose={vi.fn()} onSent={sent} />,
  );
  await fill(user);
  await user.click(screen.getByRole("button", { name: "Send inquiry" }));
  await screen.findByRole("alert");
  const title = screen.getByRole("textbox", { name: "Project title" });
  expect(title).toBeDisabled();
  await user.type(title, "Changed portal");
  expect(title).toHaveValue(payload.subject);
  first.unmount();
  render(
    <InquiryForm auth={auth} provider={ava} onClose={vi.fn()} onSent={sent} />,
  );
  expect(screen.getByRole("textbox", { name: "Project title" })).toHaveValue(
    payload.subject,
  );
  expect(screen.getByRole("textbox", { name: "Project title" })).toBeDisabled();
  await user.click(
    screen.getByRole("button", { name: "Retry original inquiry" }),
  );
  await waitFor(() => expect(sent).toHaveBeenCalledOnce());
  const firstOptions = fetch.mock.calls[0][1] as RequestInit;
  const retryOptions = fetch.mock.calls[1][1] as RequestInit;
  expect(retryOptions.body).toBe(firstOptions.body);
  expect(retryOptions.headers).toEqual(firstOptions.headers);
  expect(JSON.parse(retryOptions.body as string)).toEqual(payload);
  expect(sessionStorage.length).toBe(0);
});
it("reconciles a committed inquiry before clearing the attempt and allowing a changed new request", async () => {
  const fetch = vi
    .fn()
    .mockRejectedValueOnce(new TypeError("Lost response"))
    .mockResolvedValueOnce(reply({ ...payload, id: "committed" }))
    .mockResolvedValueOnce(reply({ id: "new" }, 201));
  vi.stubGlobal("fetch", fetch);
  const user = userEvent.setup();
  const sent = vi.fn();
  const first = render(
    <InquiryForm auth={auth} provider={ava} onClose={vi.fn()} onSent={sent} />,
  );
  await fill(user);
  await user.click(screen.getByRole("button", { name: "Send inquiry" }));
  await screen.findByRole("alert");
  await user.click(
    screen.getByRole("button", { name: "Resolve saved inquiry" }),
  );
  await waitFor(() => expect(sent).toHaveBeenCalledOnce());
  expect(sessionStorage.length).toBe(0);
  first.unmount();
  render(
    <InquiryForm auth={auth} provider={ava} onClose={vi.fn()} onSent={sent} />,
  );
  await fill(user);
  const title = screen.getByRole("textbox", { name: "Project title" });
  await user.clear(title);
  await user.type(title, "Changed customer portal");
  await user.click(screen.getByRole("button", { name: "Send inquiry" }));
  await waitFor(() => expect(sent).toHaveBeenCalledTimes(2));
  const original = fetch.mock.calls[0][1] as RequestInit;
  const newer = fetch.mock.calls[2][1] as RequestInit;
  expect(newer.headers).not.toEqual(original.headers);
  expect(JSON.parse(newer.body as string).subject).toBe(
    "Changed customer portal",
  );
  expect(fetch.mock.calls[1][0]).toBe("/api/inquiries");
  expect(fetch.mock.calls[1][1].method).toBe("POST");
  expect(fetch.mock.calls[1][1].body).toBe(original.body);
  expect(fetch.mock.calls[1][1].headers).toEqual(original.headers);
});
it("an unavailable authoritative reconciliation does not rotate the key or unlock potentially committed details", async () => {
  const fetch = vi
    .fn()
    .mockRejectedValueOnce(new TypeError("Lost response"))
    .mockResolvedValueOnce(
      reply({ message: "Request outcome unavailable" }, 503),
    );
  vi.stubGlobal("fetch", fetch);
  const user = userEvent.setup();
  render(
    <InquiryForm
      auth={auth}
      provider={ava}
      onClose={vi.fn()}
      onSent={vi.fn()}
    />,
  );
  await fill(user);
  await user.click(screen.getByRole("button", { name: "Send inquiry" }));
  await screen.findByRole("alert");
  await user.click(
    screen.getByRole("button", { name: "Resolve saved inquiry" }),
  );
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Delivery is unconfirmed",
  );
  expect(screen.getByRole("textbox", { name: "Project title" })).toBeDisabled();
  expect(
    screen.getByRole("button", { name: "Retry original inquiry" }),
  ).toBeEnabled();
});
it("a definitive rejected request allows correction with a fresh logical attempt key", async () => {
  const fetch = vi
    .fn()
    .mockResolvedValueOnce(reply({ message: "Budget rejected" }, 400))
    .mockResolvedValueOnce(reply({ id: "new" }, 201));
  vi.stubGlobal("fetch", fetch);
  const user = userEvent.setup();
  render(
    <InquiryForm
      auth={auth}
      provider={ava}
      onClose={vi.fn()}
      onSent={vi.fn()}
    />,
  );
  await fill(user);
  await user.click(screen.getByRole("button", { name: "Send inquiry" }));
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "request was rejected",
  );
  const title = screen.getByRole("textbox", { name: "Project title" });
  expect(title).toBeEnabled();
  await user.clear(title);
  await user.type(title, "Changed portal");
  await user.click(screen.getByRole("button", { name: "Send inquiry" }));
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(2));
  expect(fetch.mock.calls[1][1].headers).not.toEqual(
    fetch.mock.calls[0][1].headers,
  );
  expect(JSON.parse(fetch.mock.calls[1][1].body).subject).toBe(
    "Changed portal",
  );
});

it("never treats an identical historical inquiry as delivery of the current uncertain key", async () => {
  const historical = {
    ...payload,
    id: "historical-inquiry",
    createdAt: "2026-01-01T00:00:00Z",
  };
  let posts = 0;
  const fetch = vi
    .fn()
    .mockImplementation((_path: string, options?: RequestInit) => {
      if (options?.method !== "POST")
        return Promise.resolve(reply([historical]));
      posts++;
      if (posts <= 2)
        return Promise.reject(
          new TypeError("Current request outcome remains uncertain"),
        );
      return Promise.resolve(reply({ ...payload, id: "current-inquiry" }, 201));
    });
  vi.stubGlobal("fetch", fetch);
  const user = userEvent.setup();
  const sent = vi.fn();
  render(
    <InquiryForm auth={auth} provider={ava} onClose={vi.fn()} onSent={sent} />,
  );
  await fill(user);
  await user.click(screen.getByRole("button", { name: "Send inquiry" }));
  await screen.findByRole("alert");
  const saved = sessionStorage.getItem(sessionStorage.key(0)!);
  await user.click(
    screen.getByRole("button", { name: "Resolve saved inquiry" }),
  );
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Current request outcome remains uncertain",
  );
  expect(sent).not.toHaveBeenCalled();
  expect(sessionStorage.getItem(sessionStorage.key(0)!)).toBe(saved);
  expect(screen.getByRole("textbox", { name: "Project title" })).toBeDisabled();
  expect(fetch.mock.calls.every((call) => call[1]?.method === "POST")).toBe(
    true,
  );
  expect(fetch.mock.calls[1][1].body).toBe(fetch.mock.calls[0][1].body);
  expect(fetch.mock.calls[1][1].headers).toEqual(
    fetch.mock.calls[0][1].headers,
  );
  await user.click(
    screen.getByRole("button", { name: "Retry original inquiry" }),
  );
  await waitFor(() => expect(sent).toHaveBeenCalledOnce());
  expect(sessionStorage.length).toBe(0);
  expect(fetch.mock.calls[2][1].headers).toEqual(
    fetch.mock.calls[0][1].headers,
  );
});

it("preserves prior uncertainty when a later retry or reconciliation is rejected before reaching the database", async () => {
  const fetch = vi
    .fn()
    .mockRejectedValueOnce(new TypeError("Response lost after possible commit"))
    .mockResolvedValueOnce(
      reply({ message: "Token expired before retry" }, 401),
    )
    .mockResolvedValueOnce(reply({ message: "Reconciliation forbidden" }, 403));
  vi.stubGlobal("fetch", fetch);
  const user = userEvent.setup();
  const sent = vi.fn();
  render(
    <InquiryForm auth={auth} provider={ava} onClose={vi.fn()} onSent={sent} />,
  );
  await fill(user);
  await user.click(screen.getByRole("button", { name: "Send inquiry" }));
  await screen.findByRole("alert");
  const saved = sessionStorage.getItem(sessionStorage.key(0)!);
  await user.click(
    screen.getByRole("button", { name: "Retry original inquiry" }),
  );
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "session has expired",
  );
  expect(sessionStorage.getItem(sessionStorage.key(0)!)).toBe(saved);
  expect(screen.getByRole("textbox", { name: "Project title" })).toBeDisabled();
  expect(
    screen.queryByRole("button", { name: "Send inquiry" }),
  ).not.toBeInTheDocument();
  await user.click(
    screen.getByRole("button", { name: "Resolve saved inquiry" }),
  );
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Reconciliation forbidden",
  );
  expect(sessionStorage.getItem(sessionStorage.key(0)!)).toBe(saved);
  expect(screen.getByRole("textbox", { name: "Project title" })).toBeDisabled();
  expect(sent).not.toHaveBeenCalled();
  expect(fetch.mock.calls[2][1].headers).toEqual(
    fetch.mock.calls[0][1].headers,
  );
  expect(fetch.mock.calls[2][1].body).toBe(fetch.mock.calls[0][1].body);
});
