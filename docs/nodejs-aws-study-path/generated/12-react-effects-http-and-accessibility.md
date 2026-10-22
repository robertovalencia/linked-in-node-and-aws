---
title: "React tools: effects, abort, HTTP errors and portals"
topic: "React tools: effects, abort, HTTP errors and portals"
last_researched: 2026-10-22
source_labels: Project code; Library mechanics; Practice extensions explicitly labeled
---

# React tools: effects, abort, HTTP errors and portals

Prerequisites: lesson 11 and promise basics. Focus on the mechanics of browser-side I/O.

Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## Effect setup and cleanup

**What:** An effect synchronizes a render with an external system. Cleanup undoes that render’s subscription, timer or request ownership.

**How:** The provider-list effect creates an AbortController and returns its abort operation. Dependencies determine when a new setup replaces the previous one.

**Real code:** [frontend/src/hooks/useMarketplace.ts · lines 57–63](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L57-L63).

```ts
const controller = new AbortController();
setLoading(true);
setError("");
const params = new URLSearchParams({
  q: search,
  sort,
  page: String(page),
```

**Watch for:** A user-triggered POST belongs in an event handler rather than an accidental mount effect.

### Why does cleanup matter under StrictMode?

Development setup/cleanup checks expose effects that fail to undo their external work.

## Abort plus stale-response guards

**What:** Abort requests cancellation, but a transport or already-resolved promise may still reach application callbacks.

**How:** The hook checks signal.aborted before changing state. An old response must not replace the newer search result after filter changes.

**Real code:** [frontend/src/hooks/useMarketplace.ts · lines 73–76](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L73-L76).

```ts
  if (controller.signal.aborted) return;
  setProviders(r.items);
  setTotal(r.total);
})
```

**Watch for:** Aborting a write response wait cannot roll back a transaction already committed on the server.

### Why use both abort and a signal check?

One asks the transport to stop; the other protects state application in the callback.

## fetch errors versus HTTP rejection

**What:** fetch normally resolves for HTTP error statuses. The helper checks res.ok and throws a structured ApiError.

**How:** ApiError retains the status for callers. The helper parses public detail where possible and treats 204 as no content; api<T> does not validate the runtime response shape.

**Real code:** [frontend/src/services/http.ts · lines 24–29](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/services/http.ts#L24-L29).

```ts
if (!res.ok) {
  let detail = "The request could not be completed.";
  try {
    const e = await res.json();
    detail =
      e.detail ||
```

**Watch for:** A generic type annotation is not a JSON decoder.

### Why not rely on fetch.catch for a 403?

The response arrived successfully at the transport layer; the application must check its HTTP status.

## Storage and transport recovery

**What:** localStorage persists within an origin; sessionStorage is scoped to a browsing session/tab context. Both are readable by page JavaScript.

**How:** The retry hook stores the exact key and payload before sending. This records uncertain intent, not a confirmed business record; a retry preserves both.

**Real code:** [frontend/src/hooks/useInquiryAttempt.ts · lines 58–64](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useInquiryAttempt.ts#L58-L64).

```ts
const canonical = attempt || { key: crypto.randomUUID(), payload };
// Persist before sending: dismiss/reopen and page reload must resume this attempt.
sessionStorage.setItem(key, JSON.stringify(canonical));
setAttempt(canonical);
inFlight.current = true;
setBusy(true);
setError("");
```

**Watch for:** Do not replace an uncertain retry with a new key merely because a request timed out.

### Why store the payload as well as the key?

Reusing a key with modified content must conflict; recovery needs the original logical submission.

## Portals and DOM ownership

**What:** createPortal renders React children into a different DOM container without removing them from their React ownership tree.

**How:** The modal renders under document.body. Effects manage focus, keyboard listeners, background isolation and scroll cleanup; ARIA attributes alone do not implement those behaviors.

**Real code:** [frontend/src/components/common/Modal.tsx · lines 96–101](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/components/common/Modal.tsx#L96-L101).

```tsx
return createPortal(
  <div
    ref={backdropRef}
    className="modal-backdrop"
    role="presentation"
    onMouseDown={(e) => {
```

**Watch for:** An icon component from lucide-react still needs an accessible name on its interactive control.

### Does a portal automatically trap focus?

No. The modal’s keyboard and focus management implement that separately.

## Refs keep a fresh callback

**What:** A callback ref can hold the current handler while an effect retains a stable listener.

**How:** Modal updates onCloseRef when the prop changes. Its keyboard listener reads that ref, avoiding an old closure without reinstalling the entire listener on every callback change.

**Real code:** [frontend/src/components/common/Modal.tsx · lines 47–50](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/components/common/Modal.tsx#L47-L50).

```tsx
const onCloseRef = useRef(onClose);
useEffect(() => {
  onCloseRef.current = onClose;
}, [onClose]);
```

**Watch for:** An empty dependency array does not make every closed-over value stay current.

### Why not close over onClose directly forever?

A later render may supply a different callback; the old listener could otherwise keep the earlier one.

## Practice and mastery

Run the deterministic stale-response test:

```bash
npm --prefix frontend test -- src/hooks/useMarketplace.test.tsx
```

Its mocked first request resolves after the newer result. Expected: the newer provider list stays visible. In a practice copy, remove the aborted guard, observe the regression, then restore it.

**Proposed vertical lab: minRate.** This filter does not exist yet.

1. Extend Catalog’s `searchSchema` with bounded optional minRate and reject minRate above maxRate.
2. Add a parameterized JSONB numeric predicate using Catalog’s existing add helper. Preserve absent-filter behavior.
3. Add controlled input text and URLSearchParams handling in useMarketplace, plus a labeled Discovery filter control. Reset page when the filter changes.
4. Test schema rejection, combined SQL bounds, loading/error/empty/success UI states, and clearing the filter.

Expected local HTTP outcomes after the extension: minRate=100/maxRate=200 returns only rates in range; `minRate=201&maxRate=200` returns 400; a valid empty range result is 200 with empty items.

- Keyboard-test Tab, Shift-Tab, Escape and return focus on the existing modal.
- Explain why this feature changes the query contract without changing Provider’s response fields.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [React effects](https://react.dev/learn/synchronizing-with-effects)
- [ARIA modal pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
- [Project example: Effect setup and cleanup](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L57-L63)
- [Project example: Abort plus stale-response guards](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L73-L76)
- [Project example: fetch errors versus HTTP rejection](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/services/http.ts#L24-L29)
- [Project example: Storage and transport recovery](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useInquiryAttempt.ts#L58-L64)
- [Project example: Portals and DOM ownership](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/components/common/Modal.tsx#L96-L101)
- [Project example: Refs keep a fresh callback](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/components/common/Modal.tsx#L47-L50)
