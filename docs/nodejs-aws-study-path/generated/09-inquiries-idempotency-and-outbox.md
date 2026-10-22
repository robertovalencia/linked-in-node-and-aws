---
title: Inquiry transactions, retry identity and the outbox
topic: Distributed workflows
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# A timeout does not prove a failed write

Prerequisites: 03, 07–08. A client can lose a response after the server commits. Retrying with a new logical identity can create a second inquiry. Idempotency means repeating one logical operation has one intended effect; it does not mean all identical-looking requests from a user are duplicates.

## Exact creation sequence

Read backend/src/inquiries/inquiries.service.ts. create checks CLIENT role and an 8–100-character key, parses the body and hashes a canonical ordered field array with SHA-256. A transaction acquires a transaction-scoped PostgreSQL advisory lock derived from [actor.email, key]. It then searches for an existing inquiry with that client/key. Matching fingerprint returns the existing result; a different fingerprint produces 409.

Only when no previous inquiry exists does the service call catalog's internal provider endpoint. This HTTP call is inside the transaction and lock, with AbortSignal.timeout(5000). The response is parsed with Zod. It supplies the provider's private recipient email and public name without letting the client select an arbitrary recipient email. The service creates UUIDs, inserts the inquiry, inserts the event into outbox, and commits through Database.transaction.

The migration adds UNIQUE(client_email,idempotency_key). PostgreSQL protects the final invariant across processes; an in-memory Map would protect only one process and would disappear on restart. The advisory lock serializes the find-or-create decision for this key. Lock hash collisions can serialize unrelated keys but do not merge their stored identities.

## Browser half of the protocol

frontend/src/hooks/useInquiryAttempt.ts persists a logical attempt containing both key and canonical payload in sessionStorage before transmission. A ref prevents a same-instance double submit. An uncertain error preserves the attempt and freezes its details; retry sends the same key and same payload. A first-transmission definite rejection can clear it; rejection during retry cannot disprove an earlier commit.

This is an important source-over-docs correction: architecture.md broadly describes browser storage as token/preferences, but actual code also persists the pending inquiry payload. That is transport recovery state, not the authoritative inquiry database, and it still has privacy/retention implications. Explain its contents and lifetime rather than claiming no business text ever enters browser storage.

## Executable lab and expected outcomes

Run npm --prefix frontend test -- src/components/inquiries/InquiryAttempt.test.tsx and npm --prefix backend test -- --runTestsByPath test/workflows.spec.ts. Inspect test names and record the observed results. In a running local UI submit a synthetic inquiry while DevTools simulates a lost/failed response, reopen the attempt and retry. Confirm one inquiry ID and one logical event, not two success toasts alone. Use repository tests to simulate precise crash boundaries when network tooling cannot guarantee a post-commit loss.

Write a behavior table for same client/key/same body, same client/key/different body, different client/same key, and simultaneous duplicate requests. Expected outcomes: replay existing, 409, independent operation, and one created inquiry. Unit tests demonstrate branches; real concurrent HTTP/SQL checks are required for the lock guarantee.

## Senior reasoning

The outbox is a durable promise to publish, not immediate notification delivery. Returning a committed inquiry while Kafka is down preserves the core write but delays the inbox. Holding an external call in a DB transaction is a capacity risk. Idempotency retention, key expiry and replay policy are currently not a complete production lifecycle; specify them before adding cleanup that could permit duplicates.

Interview:

### Why hash a canonical array?

So equivalent validated fields have stable comparison independent of incoming object-key ordering.

### Why not generate a new retry key?

It would represent a new operation and can duplicate the committed one.

- [ ] Draw the lock, lookup, HTTP, insert and commit sequence correctly.
- [ ] Explain all four replay-table cases.
- [ ] Trace pending browser state separately from authoritative persistence.
- [ ] Prove retry behavior with observed IDs or focused tests.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [PostgreSQL advisory locks](https://www.postgresql.org/docs/current/explicit-locking.html#ADVISORY-LOCKS) — accessed 2026-10-22.
- [Project source: backend/src/inquiries/inquiries.service.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/inquiries/inquiries.service.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/migrations/inquiries.001.sql](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/migrations/inquiries.001.sql) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/src/hooks/useInquiryAttempt.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/src/hooks/useInquiryAttempt.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/src/components/inquiries/InquiryAttempt.test.tsx](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/src/components/inquiries/InquiryAttempt.test.tsx) — local baseline inspected 2026-10-22; private published source may lag.
