# Independent backend critic

Assessment: **WIN for the required migrated backend scope**. Original API parity, independent concurrency/ownership checks and the real broker/database restart drill pass.

## Largest gap found and repaired

The first restart drill recorded8 PASS /1 FAIL: database/application restart yielded HTTP502 through the edge because nginx retained upstream addresses after Docker service IP changes. The root repaired nginx with Docker DNS resolution and shared resolving upstream zones. `failure-drill-before-edge-repair.json` retains the failure. The final unchanged nine-check broker/database restart drill in `failure-drill.json` and `failure-drill-run.txt` now passes **9/9**, including durable inquiry creation while Kafka is stopped, delivery after recovery, duplicate event replay yielding exactly one inbox record, and database/application restart persistence through nginx without an edge restart.

## Independent actual-output evidence

I read the original `CONTRACT.md` and original48-check `scripts/acceptance.mjs`, inspected the new Nest implementation and tests without builder context, and used the running edge at `http://127.0.0.1:8180`.

- `local-acceptance.json`: root-executed original behavioral suite, exactly48 PASS /0 FAIL. The critic did not run this concurrently because its provider updates could interfere with root acceptance.
- `backend-adversarial.json`: independently executed8/8 checks.32 simultaneous same-key requests returned one inquiry ID;8 changed-body requests returned409; keys are client scoped; malformed query shapes return400; SQL metacharacter search returns an empty result; direct private lookup without key returns403; edge does not expose owner email; cross-owner status update returns403;8 conflicting terminal decisions serialize one final outcome.
- `backend-db-invariants.json`: actual PostgreSQL role matrix permits each of4 non-superuser/non-createdb/non-createrole service logins to connect only to its own service database. The critic's32-way request created exactly1 inquiry,1 published outbox row and1 inbox row. SQL uniqueness and foreign-key constraints are present.

## Code invariants reviewed

Inquiry creation uses a PostgreSQL transaction-scoped advisory lock for client/key, compares a canonical payload fingerprint, inserts the inquiry and outbox in the same transaction, and returns persisted data. Domain ownership is derived from verified JWT actor and catalog's key-protected provider lookup. Queries are parameterized. Provider ownership is locked and reputation fields remain server owned. Inquiry terminal changes and notification reads lock the row and enforce ownership. Public views omit private participant emails.

Outbox publishing locks rows with SKIP LOCKED, waits for Kafka acknowledgment, and then marks publication within the SQL transaction. A crash can replay; notification insertion uses the unique event ID and commits before the consumer callback resolves. Migrations execute under a database advisory lock, store checksums, reject applied-file mutation, and run within a transaction. This supports safe repeat initialization; it does not establish compatibility of future destructive migrations.

## Repaired gate issue

The copied acceptance script originally trusted zero failures despite conditional branches. The root repaired it to require48 passes and48 executed checks and emit `expected:48`. That enforces the documented bar for local CI and cloud acceptance; no checks were removed. A misleading identity comment about an AWS ingress rate rule was corrected.

## Scope boundaries

Shared HS256 verification keys and synthetic demo accounts are documented private-development compromises. Poison-event operational recovery, production key rotation and production high availability are not established by these checks. AWS deployment is reviewed separately in `infra-critic.md` and must not be inferred from local backend evidence.

## Final decision

After the exact48 gate and edge DNS repairs, no remaining blocker was found against the required migrated backend contract. The final real drill confirms restart-safe migration/data initialization and broker recovery while preserving the original API checks. The32-way independent concurrency probe and database constraint/role inspection strengthen the comparison beyond happy-path parity. These results support WIN for the required development migration scope, not a production reliability or deployed-AWS claim.
