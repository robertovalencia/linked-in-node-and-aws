import { act, renderHook, waitFor } from "@testing-library/react";
import type { PropsWithChildren } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AuthProvider } from "../contexts/AuthContext";
import { ava, leo, reply } from "../test/fixtures";
import { useMarketplace } from "./useMarketplace";
const wrapper = ({ children }: PropsWithChildren) => (
  <AuthProvider>{children}</AuthProvider>
);
afterEach(() => vi.unstubAllGlobals());
describe("request isolation", () => {
  it("ignores late search results after filters change even if transport ignores abort", async () => {
    let resolveFirst!: (value: Response) => void;
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockImplementationOnce(
          () =>
            new Promise<Response>((resolve) => {
              resolveFirst = resolve;
            }),
        )
        .mockResolvedValue(reply({ items: [leo], total: 1 })),
    );
    const { result } = renderHook(useMarketplace, { wrapper });
    act(() => result.current.setSearch("DevOps"));
    await waitFor(() => expect(result.current.providers).toEqual([leo]));
    await act(async () => {
      resolveFirst(reply({ items: [ava], total: 1 }));
    });
    expect(result.current.providers).toEqual([leo]);
  });
  it("does not reopen closed profiles after a delayed detail response", async () => {
    let resolveProfile!: (value: Response) => void;
    vi.stubGlobal(
      "fetch",
      vi.fn().mockImplementation((path: string) =>
        path.includes("/ava")
          ? new Promise<Response>((resolve) => {
              resolveProfile = resolve;
            })
          : Promise.resolve(reply({ items: [ava], total: 1 })),
      ),
    );
    const { result } = renderHook(useMarketplace, { wrapper });
    act(() => result.current.showProvider(ava));
    await waitFor(() => expect(resolveProfile).toBeDefined());
    act(() => result.current.setSelected(null));
    await act(async () => {
      resolveProfile(reply(ava));
    });
    expect(result.current.selected).toBeNull();
  });
  it("validates comparison storage and keeps the original project namespace untouched", () => {
    localStorage.setItem("expertly-compare", '["original"]');
    localStorage.setItem("expertly-node-aws-compare", '{"unexpected":true}');
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(reply({ items: [], total: 0 })),
    );
    const { result } = renderHook(useMarketplace, { wrapper });
    expect(result.current.compare).toEqual([]);
    expect(localStorage.getItem("expertly-compare")).toBe('["original"]');
  });
});
