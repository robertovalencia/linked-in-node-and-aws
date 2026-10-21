# Independent frontend repair recheck

Assessment: **WIN for the repaired frontend source and regression scope**. The real restart drill passes9/9 and the root-executed live desktop/mobile browser journeys pass2/2. This reviewer did not implement the frontend repairs.

I read the original independent frontend critique, the repaired Login, inquiry hook/form, notification hook/dialog, Editor, Dashboard, nginx configuration and regression tests. Executed focused Vitest tests for InquiryAttempt, Notifications, Workspace and MarketplaceRoute: **18/18 PASS across4 files** on final repaired source (log: `frontend-critic-recheck-tests.txt`). These use controlled responses and do not substitute for the root's upcoming real-stack browser journey.

## Largest gaps found and repaired

The initial repair in `frontend/src/hooks/useInquiryAttempt.ts` reconciled by searching the entire inquiry list for matching provider/title/message/budget/client type. A historical identical inquiry is not evidence that the currently uncertain idempotency key committed. The match called `finish()`, deletes the saved key and shows successful delivery. This could falsely confirm an uncommitted attempt or allow a second attempt while the first is still processing.

Required repair, now verified in source and regression tests: resolve through `inquiryService.create(auth, attempt.key, attempt.payload)`, whose server result is authoritative for that logical key, or implement an explicit owner-scoped backend key lookup. A payload match may be displayed as a possible match but must not clear the saved attempt. A new regression exposes a historical identical inquiry through any list GET, confirms no such GET is used, preserves uncertainty through another lost response, and clears only on authoritative same-key POST success.

Related key-retention gap: definitive rejection of a *later retry* (for example401 after token expiry) does not prove an earlier uncertain request did not commit. The initial repair cleared saved state on such responses regardless of attempt history. The final source uses `!attempt` to limit automatic rejection cleanup to a first transmission. Only a definitive rejection of the first transmission can automatically unlock a new key; preserve previously uncertain key/payload until authoritative success. The new lost-response → retry401 → reconciliation403 test verifies the exact original key/payload remain saved and fields stay frozen.

## Repairs confirmed by source and tests

- Pending login creates an AbortController, aborts on close/unmount, and checks both the abort signal and current request identity before mutating auth. The delayed response regression deliberately ignores cancellation and still cannot authenticate after dismissal.
- Inquiry submission now freezes key and canonical payload before transmission, persists them per actor/provider in session storage and restores across form close/reopen. The lost-response retry test verifies identical body and headers, and definitive *first* rejection can start a corrected new request. Both reconciliation caveats above are repaired and covered by passing regressions.
- Notification list fetch depends on opening the dialog and has loading/error/retry states with cancellation guards. The regression starts empty then returns a new arrival on opening; a503 refresh shows an error rather than an empty-inbox success.
- Editor and Dashboard terminate failed initial loading, offer retry, separate failure from successful empty state and abort stale list effects. Regression tests verify those states.
- nginx now declares Docker DNS resolver, shared upstream zones and resolving service entries. The root's final real restart drill passes9/9, including recovery through nginx after service container addresses change; no edge restart is needed. Its earlier failure is retained separately.

The original secondary accessibility-tree isolation and expired-session recovery observations remain documented limitations unless separately addressed; no assistive-technology validation is claimed here.

## Final source re-review

The final hook resolves delivery only by POSTing the saved key and canonical payload to the authoritative idempotency endpoint. It no longer infers identity from matching historical content. A definitive rejection clears state only when no prior attempt existed, so later auth/validation errors preserve earlier uncertainty. Both new regressions passed in this independent re-run. No remaining blocker was found in the requested repair scope. Real browser journeys and dependency restart behavior must be evaluated from their own evidence rather than these controlled-response tests.

## Integrated evidence reviewed

`browser-smoke.json` records actual nginx journeys at desktop and390px mobile: six persisted providers, no page horizontal overflow, comparing two profiles, rich profile content, client login, durable inquiry submission and no browser errors. Both pass. `failure-drill.json` independently covers the dependency recovery boundary at9/9. These are root-executed evidence reviewed here, not an additional browser run by this critic. Provider editing/status and post-login notification-arrival regressions have controlled component evidence plus original backend HTTP acceptance; a real browser provider journey is not claimed by the two browser smoke entries. Blind visual assessment is separate in `visual-critic.md`.
