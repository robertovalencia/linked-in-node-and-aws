---
title: HTTP contracts, Zod validation and errors
topic: API contracts
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# Make the boundary explicit

Prerequisites: 02, 04, 05. An API contract describes what callers send, what the server returns, who may call it and how failures behave. A TypeScript interface is only one part. Read CONTRACT.md alongside controllers and scripts/acceptance.mjs; implementation discrepancies are findings to resolve, not permission to invent behavior.

## Walk through validation

backend/src/inquiries/inquiries.controller.ts receives body: unknown and a possibly missing Idempotency-Key. InquiriesService.create verifies CLIENT role, checks the key format, and calls inquirySchema.parse. The resulting input has been checked at runtime. Catalog search receives URL query strings; searchSchema deliberately coerces selected numeric fields and handles the available flag. A query string of available=false must not become Boolean('false'), which is true in JavaScript.

Zod errors become 400 via backend/src/common/errors.ts. Known Nest HttpExceptions preserve their status, parser failures recognize 400/413, and unexpected failures return a generic 500 detail while logging server-side information. The filter bounds public detail length. Never return database connection strings, raw SQL internals or stack traces to the browser.

Route specificity matters: /api/providers/me is declared before /api/providers/:id. Public GET returns a profile document without ownerEmail. The internal lookup returns ownerEmail only after its internal-key check and is omitted from frontend proxy routing. Hiding a path in the UI is not authentication; the backend still enforces the key.

## Executable contract lab

With the local environment running, execute:

~~~bash
curl -i 'http://127.0.0.1:8180/api/providers?page=0&size=2&available=false'
curl -i 'http://127.0.0.1:8180/api/providers?page=-1'
curl -i -H 'Content-Type: application/json' -d '{"email":"bad","password":"x"}' http://127.0.0.1:8180/api/auth/login
~~~

Expect a JSON page with at most two items for the first request, validation failure 400 for the invalid page and email, and no leaked stack trace. Verify exact pagination bounds in provider.schema.ts before choosing additional inputs. Save status and body in your evidence notebook. Run npm run acceptance for the repository's full HTTP contract when local dependencies are ready; a documented 48-check suite is a target until your own output confirms it.

## Extension exercise

Specify cursor pagination as a proposal without changing the current page/size contract. Define sorting stability, cursor expiry/encoding, maximum size and backward compatibility. For a new field add a contract example, runtime schema, UI type, SQL mapping and behavioral test. Changing only the interface is incomplete.

## Debugging and senior reasoning

If the UI shows “could not complete,” inspect the Network tab status/body, then api<T>'s error normalization, then ErrorFilter. A 404 can mean missing path or missing resource; request method and exact URL help distinguish them. A 401 concerns identity, a 403 permission, and a 409 a conflict with current state or the idempotency contract. Do not turn every failure into 200 with an error string; callers and monitoring depend on meaningful status.



### PUT versus PATCH?

PUT commonly represents replacing a resource representation; PATCH applies a defined partial modification. Here profile PUT accepts the editable profile document, and status PATCH performs a constrained transition.

### Why validate twice?

UI validation helps the user; backend validation protects the server because callers can bypass the UI.

- [ ] Trace invalid input into its public status and detail.
- [ ] Explain coercion and why types do not validate JSON.
- [ ] Show that public profiles do not expose ownerEmail.
- [ ] Specify a contract extension with compatibility and negative tests.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [Zod documentation](https://zod.dev/) — accessed 2026-10-22.
- [Nest exception filters](https://docs.nestjs.com/exception-filters) — accessed 2026-10-22.
- [HTTP semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) — accessed 2026-10-22.
- [Project source: CONTRACT.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/CONTRACT.md) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/common/errors.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/common/errors.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/catalog/provider.schema.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/catalog/provider.schema.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/inquiries/inquiry.schema.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/inquiries/inquiry.schema.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: scripts/acceptance.mjs](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/scripts/acceptance.mjs) — local baseline inspected 2026-10-22; private published source may lag.
