import { afterEach, describe, expect, it, vi } from "vitest";
import { reply } from "../test/fixtures";
import { api } from "./http";
import { inquiryService } from "./marketplace";
const auth = {
  token: "token",
  id: "client",
  name: "Client",
  email: "client@demo.local",
  role: "CLIENT" as const,
};
afterEach(() => vi.unstubAllGlobals());
describe("HTTP boundary", () => {
  it("explains expired authentication and validation failures", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValueOnce(reply({}, 401))
        .mockResolvedValueOnce(
          reply(
            { message: ["subject must be longer", "budget must be positive"] },
            400,
          ),
        ),
    );
    await expect(api("/private", auth)).rejects.toThrow("session has expired");
    await expect(api("/form")).rejects.toThrow(
      "subject must be longer; budget must be positive",
    );
  });
  it("supports empty successful responses and non-JSON failures", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValueOnce(reply(null, 204))
        .mockResolvedValueOnce(new Response("Bad gateway", { status: 502 })),
    );
    await expect(api("/read")).resolves.toBeUndefined();
    await expect(api("/bad")).rejects.toThrow("request could not be completed");
  });
  it("sends authorization and a stable idempotency key when creating inquiries", async () => {
    const fetch = vi.fn().mockResolvedValue(reply({ id: "inquiry" }, 201));
    vi.stubGlobal("fetch", fetch);
    await inquiryService.create(auth, "retry-key", {
      providerId: "ava",
      subject: "Project",
      message: "Build my application",
      budget: 1000,
      clientType: "INDIVIDUAL",
    });
    expect(fetch).toHaveBeenCalledWith(
      "/api/inquiries",
      expect.objectContaining({
        method: "POST",
        headers: expect.objectContaining({
          Authorization: "Bearer token",
          "Idempotency-Key": "retry-key",
        }),
      }),
    );
  });
});
