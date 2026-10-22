---
title: React effects, HTTP races, sessions and accessible dialogs
topic: React reliability
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# External synchronization needs cleanup

Prerequisites: 03, 08–11. Rendering computes the UI. An effect synchronizes it with a network request, timer, browser storage or DOM listener. A user-triggered submission belongs in an event handler; performing it in a mount effect risks duplicate/accidental actions.

## Follow a real effect

frontend/src/hooks/useMarketplace.ts creates an AbortController for each provider-list effect, builds URLSearchParams and calls providerService.list with its signal. It checks signal.aborted before updating state and aborts on cleanup. Rapid filter changes should not let an old response replace newer results. The dependencies describe values used by the effect; suppressing the hooks lint rule conceals bugs rather than resolving dependencies.

AuthContext restores a saved token using identityService.me. It also checks that the stored token still matches before applying its result, preventing an old restore response from overwriting a newer session. Abort alone is not a business cancellation guarantee: aborting a POST response wait does not undo a committed inquiry. useInquiryAttempt consequently persists a retry identity and payload separately.

services/http.ts adds JSON and bearer headers, normalizes non-OK errors into ApiError, maps 401 to a session message and handles 204. fetch generally resolves even for HTTP 4xx/5xx, so res.ok must be checked. The generic T is compile-time only. Network rejection, abort and HTTP rejection have different meanings and must not all be labeled “server never received it.”

## Accessible dialogs are lifecycle work

components/common/Modal.tsx uses createPortal from react-dom so the dialog is rendered under document.body. Refs access dialog/backdrop DOM nodes and hold the latest onClose callback. Effects register keyboard handling, move initial focus, trap Tab, handle Escape for the top dialog, mark background content inert/aria-hidden, lock scrolling and restore focus/state on cleanup. A module-level stack coordinates multiple open dialogs. lucide-react supplies icons; icon-only controls still need accessible names.

## Executable lab

Run npm --prefix frontend test -- src/hooks/useMarketplace.test.tsx src/contexts/AuthContext.test.tsx src/components/common/Modal.test.tsx src/services/http.test.ts. In the local browser, enable slow network, rapidly change category and search, then verify final results match the newest filters. Open a modal entirely by keyboard, cycle Tab and Shift-Tab, press Escape and confirm focus returns to the opener. Open a nested dialog if the UI exposes one and confirm only the top responds. Automated tests and real keyboard observation answer different questions.

For a practice bug remove the aborted check in a scratch copy and arrange an older request to resolve last using a deterministic mocked promise. Write a test that fails with stale data and passes after restoring the guard. Do not depend on unpredictable Internet latency for this test.

## Senior tradeoffs

Cancellation limits unnecessary work but does not provide server rollback. A query-cache library could centralize retries, caching and request identity, but is not an existing dependency. Refs do not trigger renders; use state when the display must update. An effect holding a stale callback can call outdated code, while an unstable callback dependency can repeatedly tear down listeners. This Modal uses a ref to retain the current callback without reinstalling the whole keyboard effect for every render.

## Proposed vertical lab: minimum hourly rate

This feature does not exist yet. Existing search has maxRate. Add optional minRate while preserving behavior when it is absent. Work in a practice branch. Trace one input through every layer rather than adding a disconnected React demo.

1. In backend/src/catalog/provider.schema.ts extend searchSchema with minRate using the same integer/coercion/bounds convention as maxRate. Reject minRate above maxRate when both exist; do not silently swap values. Add schema tests in a new backend/test/min-rate.spec.ts.
2. In backend/src/catalog/catalog.service.ts add a parameterized JSONB hourlyRate >= predicate using the existing add helper. Retain fixed sort selection and stable pagination. Add behavior tests proving absent minRate preserves current results and bounds combine correctly.
3. In frontend/src/hooks/useMarketplace.ts add controlled input text state minRate, set it in URLSearchParams only when nonempty, add it to the provider-list effect dependencies, return its getter/setter and reset page when the filter changes. Existing providerService.list accepts URLSearchParams, so no invented typed DTO parameter should be added unless you deliberately introduce one.
4. In frontend/src/components/discovery/Discovery.tsx, the actual filter panel, add a labeled minimum-rate numeric input using the hook's state. If the prop plumbing is defined elsewhere, follow MarketplaceRoute.tsx and its MarketplaceState type rather than assuming context. Keep empty text distinct from numeric zero. No response type change is required because Provider already includes hourlyRate.
5. In frontend/src/hooks/useMarketplace.test.tsx assert the service receives minRate and resets page as specified. In a component test assert labeled input interaction and visible loading/error/empty/success behavior. In frontend/src/services/http.test.ts retain correct 400 detail handling.

With local services up, run curl -i 'http://127.0.0.1:8180/api/providers?minRate=100&maxRate=200' and verify every returned rate is within bounds; expect 400 for minRate=201&maxRate=200. Test a valid range with no matches as 200 with empty items, not a server error. From the UI type a minimum, submit/apply through the actual filter interaction and observe Network query, loading state and returned cards. Clear it and prove the original default results return. Run npm run check, npm test and npm run build, then add the real HTTP case to an explicit extension test rather than pretending the original 48-check reference suite already covered it.

Interview:

### Why does StrictMode expose effect bugs?

Development remount/re-execution checks expose missing cleanup; write effects that tolerate setup/cleanup rather than disabling diagnostics.

### Is ARIA enough?

No; semantic names, focus behavior, keyboard access and background isolation must work together.

- [ ] Explain fetch rejection versus HTTP error versus abort.
- [ ] Reproduce and prevent stale-response overwrite deterministically.
- [ ] Keyboard-test focus, Escape and restoration.
- [ ] Explain state, refs, effects, portals and stable callbacks in source.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [React effects](https://react.dev/learn/synchronizing-with-effects) — accessed 2026-10-22.
- [WAI-ARIA modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) — accessed 2026-10-22.
- [Project source: frontend/src/hooks/useMarketplace.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/src/hooks/useMarketplace.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/src/contexts/AuthContext.tsx](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/src/contexts/AuthContext.tsx) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/src/services/http.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/src/services/http.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/src/components/common/Modal.tsx](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/src/components/common/Modal.tsx) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/src/components/discovery/Discovery.tsx](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/src/components/discovery/Discovery.tsx) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/catalog/provider.schema.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/catalog/provider.schema.ts) — local baseline inspected 2026-10-22; private published source may lag.
