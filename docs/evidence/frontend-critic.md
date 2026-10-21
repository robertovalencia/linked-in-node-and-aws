# Independent frontend and learning-document review

Review time: 2026-10-21. Verdict: **NO WIN yet; repair the three reproduced defects below.**

The new implementation is substantially easier to navigate than the reference's 1,900-line `frontend/src/main.tsx`: rendering components, HTTP/service functions, contracts, auth context and page effects are separated into actual imported modules. Search, detail and comparison effects now suppress stale results; auth restoration checks that the stored token still matches. These are meaningful improvements. The remaining god-hook/page-state spread is a maintainability limitation, but not itself a blocker for this small single-page product.

## Independent evidence

- Ran `npm run check && npm test` in `frontend`: ESLint, Prettier, strict TypeScript and all **16 tests across seven files passed**.
- Read the tests themselves: they cover search/detail stale responses, auth restore, comparison storage, successful anonymous-contact/login/inquiry, profile edit, status update success/failure, notification read and stacked Escape handling. They do not cover the three failures below.
- Reproduced the failures in headless Google Chrome against an independently started Vite preview on `127.0.0.1:5185`, with browser interception controlling realistic response timing/errors. The fixture script was `/tmp/frontend-critic.mjs`; no application code was changed. This proves browser behavior under those responses, not the database/broker implementation.
- Attempted a separate real-stack browser check at `http://localhost:8180`; the connection was refused at that time. Docker/API/persistence parity is therefore not claimed by this review.

## Blocking findings

### P1 — Uncertain inquiry failure has no safe edited-payload recovery

Source: `frontend/src/components/inquiries/InquiryForm.tsx:26,39`; the key is created once per mounted form, while every submit reads the currently editable fields.

Reproducer: submit a valid inquiry; let the server commit it but abort the browser response (a lost response is a normal uncertain outcome). The error leaves fields editable. Change the title from `Customer portal` to `Changed portal` and submit again. The browser sends the **same idempotency key with a different body**. A correct server responds 409; the form shows the conflict without recovery. Closing and reopening creates a new key and can silently create a second inquiry even though the first already committed.

Observed browser output: `sameKey: true`, subjects `["Customer portal", "Changed portal"]`, error `Idempotency key was already used with another payload`.

Required repair: keep a logical submission's key and canonical payload together; make transport retry repeat that payload. Give an explicit way to reconcile the uncertain outcome before starting a changed request. Do not fix this by blindly rotating a key after every failure. Add a browser/component test for lost success response plus safe retry, and for changing fields after uncertain failure.

### P2 — Closing a pending sign-in does not cancel its auth side effect

Source: `frontend/src/components/auth/Login.tsx:32` calls the parent's `onLogin` after awaiting the request, even after the dialog unmounts.

Reproducer: submit login with its response delayed; close the dialog using its close button; resolve the login successfully. The page nevertheless authenticates and persists the token. Observed: `canceledLoginStillAuthenticated: true` (Sign out appeared after dialog dismissal). A late earlier login can also overwrite a newer sign-in.

Required repair: abort when possible and always suppress post-unmount/stale completion, since an abort alone does not guarantee the transport honors it. Add a regression test that closes a pending login, then resolves it and verifies no auth mutation. R08 explicitly asks for stale-response handling.

### P2 — Provider notification inbox remains stale after new inquiries arrive

Source: `frontend/src/hooks/useMarketplace.ts:80–98` fetches only on auth/reload; `frontend/src/components/notifications/NotificationsDialog.tsx` only renders the cached list. Opening the bell does not fetch.

Reproducer: provider signs in while inbox is empty; another client sends an inquiry; provider opens Notifications. The browser performs no second GET and says “You're all caught up.” Closing/reopening does not help. A hard reload/sign-out/sign-in is needed even though the broker has delivered the event.

Observed: `notificationRequests: 1`, `showsAllCaughtUp: true` after opening the dialog, while the intercept would return the new notification on any subsequent GET.

Required repair: refresh on opening (with loading/error state and stale-result protection); polling/focus refresh can also keep the bell current. Ensure refresh failures do not masquerade as successful empty inboxes. Test the post-login arrival path. The reference also had this limitation, but carrying it forward does not win the eventual-notification product journey or the new loading/error requirement.

## Secondary repair opportunities

- `components/profile/Editor.tsx:22–33`: initial GET failure leaves `p` null, so the dialog renders both an error and Loading indefinitely, with no retry. Show a terminal load error and retry.
- `components/inquiries/Dashboard.tsx:21–29`: failed GET renders the error followed by success-style empty-inbox copy and no retry. Separate pending/failure/empty states. These list/editor effects also lack stale/auth-change cleanup.
- `components/common/Modal.tsx`: keyboard Tab/Escape management is improved for stacked dialogs, but multiple `aria-modal=true` dialogs and the background remain exposed to assistive technology. An inert/hidden background or native modal handling would complete the model; the single existing modal test only verifies Escape and body scrolling, not focus cycling or accessibility-tree isolation.
- After token expiry during a session, HTTP errors tell the user to sign in again, but auth state remains signed in and the normal Sign in button is unavailable until explicit logout. A centralized unauthorized-session action would make recovery coherent.

## Learning-document assessment

Read `docs/specs/requirements.md`, `architecture.md`, `local-setup.md`, `ai-development.md`, `interview-demo.md`, `testing.md`, and frontend/Java-to-Nest interview guides against actual imports/source.

The material appropriately distinguishes browser guards from server authorization, typed contracts from runtime validation, local checks from cloud deployment, HMAC laboratory compromise from production design, at-least-once delivery from exactly-once, and an AI-generation target from audited measurement. It is useful interview scaffolding rather than a misleading claim of production experience.

The frontend guide's “one idempotency key per logical attempt” is the right intended design, but the form currently equates component lifetime with logical attempt despite editable payloads. Its stale-response discussion is true for catalog/auth-restore effects but does not cover pending login, editor or workspace requests. The notification architecture diagram describes backend delivery; it should not be presented as evidence that a mounted browser inbox observes delivery until the refresh defect is fixed.

At review time, `README.md`, `docs/traceability.md`, `docs/reviews.md` and `docs/results.md` were not yet present despite guide links to them. These are likely concurrent documentation deliverables; recheck existence and links before final handoff. Local setup uses the intended final destination `/Users/robertovalencia/Documents/Business/linked-in-node-and-aws`, not this staging directory, so execute the final instructions in that destination before claiming reproducibility.

## Comparison and practical limit

**NO WIN pending repairs and real-stack evidence.** The code structure and targeted stale-query tests beat the reference for readability and selected async cases. Happy-path parity is plausible from source and tests, but successful mocked UI tests do not establish a live integrated journey. Re-review the fixes with regression tests and then verify discovery, compare, company inquiry, provider editing/status and fresh notification reading against the running edge/API services. Do not infer AWS or assistive-technology validation from this review.
