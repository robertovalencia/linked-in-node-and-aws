# 4. Learn by observing and recovering

[Guide index](README.md) · [Previous: the full journey](03-browser-events-and-aws.md) · [Next: glossary](05-glossary.md)

These are local learning exercises, not evidence that an author ran them. Record your date, commit, Node/Docker versions, command, expected result, actual result, and explanation.

A surprising outcome is useful evidence: diagnose it instead of editing the expected result to make a check pass.

## Before the first exercise

Use a terminal in the actual project root. No AWS account or credentials are needed.

The examples use synthetic demo accounts and create durable laboratory inquiries/notifications. There is no delete endpoint; normal cleanup stops processes while preserving those records.

```bash
cd /Users/robertovalencia/Documents/Business/linked-in-node-and-aws
node --version
npm --version
docker compose version
npm run setup
npm run up
```

Use the repository's Node 22 baseline (backend declares `>=22 <25`) and Docker Desktop with Compose v2. Startup builds images and pulls dependencies, so it needs network access.

Expect `http://localhost:8180` to show the marketplace and `docker compose ps` to show healthy services after startup. A command timing out is not a pass; inspect logs/resources.

All commands below assume full-container mode unless explicitly changing modes. The Compose project is `linked-in-node-local`. `npm run down` stops this local stack and keeps volumes.

Do not use `down --volumes` for ordinary troubleshooting. Never replace `.env` while existing PostgreSQL volumes still depend on its passwords.

## Lab 1: HTTP is a visible conversation

```bash
curl -i http://localhost:8180/api/providers
curl -i 'http://localhost:8180/api/providers?available=yes'
curl -i http://localhost:8180/api/auth/me
curl -i http://localhost:8182/health/live
curl -i http://localhost:8182/health/ready
```

Expected: 200 with `items`/`total`; 400 validation detail; 401 without a bearer token; 200 live; 200 ready when DB is reachable. An empty search array is still success.

Read readiness directly on the service port because nginx does not expose service management routes.

Request `http://localhost:8180/internal/providers/ava-martinez`, then `http://localhost:8182/internal/providers/ava-martinez`. nginx may return SPA HTML through its fallback, not private API JSON. Direct Catalog without its key should return 403 JSON.

Do not obtain or print the actual internal key for this lab.

Deliverable: table of URL, status, content type, responsible component, and why. Mastery: point to each source branch.

## Lab 2: safe retry, conflict, and authorization

Tokens stay in the following Node process's memory. It prints statuses and synthetic record IDs, not credentials.

Run the entire block from the project root after the stack is healthy:

```bash
node --input-type=module <<'JS'
import assert from 'node:assert/strict';
import { randomUUID } from 'node:crypto';
const base = 'http://localhost:8180';
async function call(path, { token, key, body, method = 'GET' } = {}) {
  const response = await fetch(base + path, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(key ? { 'Idempotency-Key': key } : {}),
    },
    ...(body === undefined ? {} : { body: JSON.stringify(body) }),
  });
  return { status: response.status, body: await response.json() };
}
async function login(email) {
  const result = await call('/api/auth/login', {
    method: 'POST', body: { email, password: 'DemoPass123!' },
  });
  assert.equal(result.status, 200, `Login failed for synthetic actor ${email}`);
  return result.body.token;
}
const client = await login('company@demo.local');
const provider = await login('ava@demo.local');
const otherProvider = await login('leo@demo.local');
const otherClient = await login('individual@demo.local');
const key = randomUUID();
const payload = {
  providerId: 'ava-martinez', subject: 'Beginner trace exercise',
  message: 'Please help build a customer portal for this local learning exercise.',
  budget: 2500, clientType: 'COMPANY',
};
const send = (body = payload) => call('/api/inquiries', {
  method: 'POST', token: client, key, body,
});
const [first, repeat] = await Promise.all([send(), send()]);
assert.equal(first.status, 201);
assert.equal(repeat.status, 201);
assert.equal(first.body.id, repeat.body.id);
console.log('Concurrent same-key requests converged:', first.body.id);
const conflict = await send({ ...payload, budget: 2600 });
assert.equal(conflict.status, 409);
console.log('Changed payload under same key:', conflict.status);
const missingKey = await call('/api/inquiries', {
  method: 'POST', token: client, body: payload,
});
assert.equal(missingKey.status, 400);
const forbidden = await call('/api/inquiries', {
  method: 'POST', token: provider, key: randomUUID(), body: payload,
});
assert.equal(forbidden.status, 403);
const unrelated = await call('/api/inquiries', { token: otherClient });
assert.equal(unrelated.status, 200);
assert.ok(!unrelated.body.some(item => item.id === first.body.id));
const path = `/api/inquiries/${first.body.id}/status`;
const wrongOwner = await call(path, {
  method: 'PATCH', token: otherProvider, body: { status: 'ACCEPTED' },
});
assert.equal(wrongOwner.status, 403);
const accepted = await call(path, {
  method: 'PATCH', token: provider, body: { status: 'ACCEPTED' },
});
assert.equal(accepted.status, 200);
assert.equal(accepted.body.status, 'ACCEPTED');
const acceptedAgain = await call(path, {
  method: 'PATCH', token: provider, body: { status: 'ACCEPTED' },
});
assert.equal(acceptedAgain.status, 200);
const incompatible = await call(path, {
  method: 'PATCH', token: provider, body: { status: 'DECLINED' },
});
assert.equal(incompatible.status, 409);
let notification;
for (let attempt = 0; attempt < 30; attempt++) {
  const inbox = await call('/api/notifications', { token: provider });
  assert.equal(inbox.status, 200);
  notification = inbox.body.find(item => item.inquiryId === first.body.id);
  if (notification) break;
  await new Promise(resolve => setTimeout(resolve, 1000));
}
assert.ok(notification, 'Notification did not arrive within this 30-second lab window');
const wrongRead = await call(`/api/notifications/${notification.id}/read`, {
  method: 'PATCH', token: otherProvider,
});
assert.equal(wrongRead.status, 403);
const read = await call(`/api/notifications/${notification.id}/read`, {
  method: 'PATCH', token: provider,
});
assert.equal(read.status, 200);
assert.equal(read.body.read, true);
console.log('Role, participant, ownership, transition and inbox checks passed.');
JS
```

Expected: two concurrent 201 responses have the same inquiry ID; changed payload gives 409; role/owner checks pass; a notification eventually appears. The 30-second wait is an observation window, not a contractual SLA.

If it fails, keep the inquiry ID, inspect broker/consumer/outbox, and recover. Re-running this block creates a **new** key and inquiry; retrying an uncertain submission instead requires its original key/payload.

Use the printed inquiry ID in these read-only checks, substituting it for `PASTE_INQUIRY_UUID` without changing the rest of the SQL:

```bash
docker compose exec -T postgres psql -U marketplace_admin -d inquiries -c "SELECT count(*) AS inquiry_rows FROM inquiries WHERE id='PASTE_INQUIRY_UUID';"
docker compose exec -T postgres psql -U marketplace_admin -d inquiries -c "SELECT count(*) AS logical_events FROM outbox WHERE inquiry_id='PASTE_INQUIRY_UUID';"
docker compose exec -T postgres psql -U marketplace_admin -d notifications -c "SELECT count(*) AS inbox_rows FROM notifications WHERE inquiry_id='PASTE_INQUIRY_UUID';"
```

Expect each count to be 1 after delivery. This proves the observed concurrent run and its durable effects, not unlimited load or every crash schedule.

It does not prove Kafka never repeated a send. Deliverable: annotate the script with methods responsible for 400/403/409 and explain each distinct identity.

## Lab 3: persistence without destructive changes

These read-only commands use the administrator inside the local PostgreSQL container. They select IDs/status/counts rather than secret columns.

Applications should keep their restricted service roles.

```bash
docker compose exec -T postgres psql -U marketplace_admin -d inquiries -c 'SELECT id,status,created_at FROM inquiries ORDER BY created_at DESC LIMIT 5;'
docker compose exec -T postgres psql -U marketplace_admin -d inquiries -c 'SELECT count(*) AS pending_outbox FROM outbox WHERE published_at IS NULL;'
docker compose exec -T postgres psql -U marketplace_admin -d notifications -c 'SELECT event_id,count(*) FROM notifications GROUP BY event_id HAVING count(*) > 1;'
docker compose exec -T postgres psql -U marketplace_admin -d inquiries -c 'SELECT version,applied_at FROM schema_migrations ORDER BY version;'
docker compose restart inquiries notifications
```

Wait for readiness, repeat the queries, and observe retained records. The duplicate query should return no rows because event ID is unique; that does not prove transport never redelivered. `pending_outbox=0` describes the instant queried.

Distinguish process memory, container filesystem, Docker volume, and independent backup.

Do not edit an applied SQL file to rerun it. A migration exercise belongs in a learning branch using a new numbered file and compatibility/recovery checks.

Reading this guide does not require changing application behavior.

## Lab 4: broker failure and recovery

Precondition: healthy full stack, a client browser signed in, and another private/incognito browser signed in as Ava. Do not run while somebody else depends on this local demo.

1. Record the pending-outbox count. Stop the broker and inspect:

   ```bash
   docker compose stop kafka
   docker compose logs --tail=40 inquiries notifications
   curl -i http://localhost:8183/health/live
   curl -i http://localhost:8183/health/ready
   ```

2. Expect live 200 while running. Ready should eventually become 503 after failure detection; an immediate check can still see a stale worker flag. Retry logs should appear. Frontend `/health` does not establish broker health.
3. Submit one valid inquiry with a distinctive subject through the client's UI. A running handler can commit if Catalog/PostgreSQL work, even while readiness fails. The provider's new inbox item should not arrive during broker outage. Query pending outbox to confirm durable intent.
4. Restore promptly:

   ```bash
   docker compose start kafka
   docker compose logs --tail=60 inquiries notifications
   curl -i http://localhost:8183/health/ready
   curl -i http://localhost:8184/health/ready
   ```

5. Allow reconnect/group join, recheck readiness/outbox, reopen or retry the provider inbox. Expected: pending intent drains and one effect appears for the event. If the consumer does not recover, preserve crash logs, then `docker compose restart notifications`. The outer loop/KafkaJS crash behavior does not establish that every fault repairs itself without an operator.

Always `docker compose start kafka` if abandoning mid-lab. Never delete volumes or mark outbox published manually to make it look repaired.

Deliverable: timeline of commit, pending intent, readiness failure, restart, consumer recovery, and visible inbox. Explain which data-loss failures remain untested.

## Lab 5: use a real breakpoint

Switch from container APIs to host development deliberately; they share ports:

```bash
npm run down
bash scripts/local.sh deps
npm --prefix backend ci
npm --prefix frontend ci
npm run dev
```

Open `http://localhost:5183` and keep that terminal running. In VS Code open this project and use [.vscode/launch.json](../../.vscode/launch.json) **Attach inquiries**, port 9231.

Identity uses 9229, Catalog 9230, Notifications 9232. Inspectors bind loopback; do not expose publicly.

Break in `InquiriesController.create`, before the advisory lock, after previous-row lookup, and at each INSERT. Submit a synthetic inquiry.

Inspect body, role, key, parsed input, and returned ID without copying credentials to evidence. Stepping over `await` pauses this function, not every request.

A breakpoint held inside a transaction also holds its connection/locks; resume promptly.

Use **Debug React** and break in `useInquiryAttempt.submit`, `inquiryService.create`, and `api`. Inspect Network URL/method/status/request/response with authorization redacted.

Deliverable: source call-chain trace, not a screenshot of a token.

Stop host processes with `Ctrl+C`, then `npm run down` to stop dependencies. Return to full mode later using `npm run up` and port 8180.

## Lab 6: stale reads versus uncertain writes

Throttle browser Network, submit one search and quickly another. Observe aborted/discarded stale responses.

Find cleanup and signal checks in `useMarketplace`; remove throttling afterward. Cancelling a browser request cannot undo a transaction already committed on the server.

Read [InquiryAttempt tests](../../frontend/src/components/inquiries/InquiryAttempt.test.tsx) and [useInquiryAttempt](../../frontend/src/hooks/useInquiryAttempt.ts). Explain why a later retry's authentication rejection cannot disprove an earlier uncertain commit.

A simulated network interruption can land at different times; establish persistence via SQL or original-key reconciliation before making claims. Do not clear saved sessionStorage intent to conceal unknown delivery.

Deliverable: two timelines, stale **read** result versus uncertain **write** outcome. Explain why cancellation addresses only one.

## Verification commands have different jobs

| Command | Evidence it supplies | Limitation |
|---|---|---|
| `npm run check` | Backend/frontend types, ESLint, Prettier | Does not prove business behavior |
| `npm test` | Jest backend and Vitest frontend behaviors | Mocks do not prove distributed persistence |
| `npm run build` | Backend emit and production UI build | Does not prove deployment |
| `npm run acceptance` | Real HTTP through local edge | Require exactly 48 passes, zero failures, not merely process success |
| `npm run test:browser` | Playwright UI journeys | Needs installed browser and healthy stack |
| `node scripts/failure-drill.mjs` | Existing local failure/security/dedup drills | Read script; mutates synthetic data; preserve failures |

Root/backend/frontend have separate manifests/locks, not npm workspaces. For root Playwright tooling run `npm ci` and, if needed, `npx playwright install chromium`.

Acceptance writes under `docs/evidence`; record your date/environment too. [Testing](../testing.md) describes the full workflow. A copied command table is not a test report.

## Diagnose by symptom

| Symptom | Inspect first | Safe next step |
|---|---|---|
| Port already in use | Host versus Compose mode | Stop the mode you are leaving |
| DB password failure after `.env` replacement | Existing volume and setup history | Restore matching config or coordinate role-password change; preserve data |
| Missing migrations directory | Working directory | Use supplied scripts; backend expects `migrations` relative to cwd |
| Migration checksum error | Named file/history | Restore immutable applied file; new change needs new migration |
| 401 | Token absent/expired | Sign in; do not weaken verification |
| 403 | Verified role and stored owner | Use correct actor; UI controls are not security boundaries |
| 409 | Changed key payload or terminal state | Reconcile original intent; do not silently generate another key |
| Missing inbox after commit | Outbox, broker, consumer, current fetch | Recover dependency and refetch; distinguish delay from loss |
| nginx works, API fails | Direct readiness/proxy path | Static health does not establish downstream health |
| Host Kafka unreachable | Listener context | Host uses 19092; containers use kafka:9092 |

## Rehearse without reading first

| Question | Minimum answer checkpoints |
|---|---|
| One backend or four? | Shared source/image; four processes/pools; service-owned data; shared-host risk |
| What does await guarantee? | Function-local Promise sequencing; no global serialization; DB locks enforce invariants |
| How do concurrent retries converge? | Client/key lock, canonical parsed fingerprint, same result or 409, unique constraint |
| Where is the transaction? | One pg client, BEGIN/COMMIT/ROLLBACK, inquiry+outbox; Catalog lookup inside and latency cost |
| Exactly-once Kafka? | No; broker-ack/SQL and SQL/offset windows; unique event identity prevents duplicate effect |
| Why isn't JWT enough? | Authentication, role, object ownership are separate |
| Why Zod with TypeScript? | Types erased; runtime JSON/event input untrusted |
| How does React avoid false success? | Await API, show failure, preserve uncertain key/payload; stale reads are separate |
| What does rollback reverse? | Prior app images when available; not schema/data; need compatibility and restore plan |
| What is on AWS? | Prepared EC2 Compose/SSM; execution evidence required; no invented RDS/MSK |
| How would you scale? | Measure first; connection/query/worker budgets, partitions/replicas, observability and cost |

Final artifact: ten-minute demo/transcript with one successful journey, one rejected ownership attempt, and a recovered broker outage. Distinguish observation, inference, and remaining uncertainty.
