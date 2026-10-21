# Implementation plan and approval boundaries

1. Inspect reference contracts, data, acceptance and actual shortcomings. Record its commit and keep credentials/history/evidence out of the new repository.
2. Port capability rules into four NestJS processes. Migrate schema/seed data, JWT verification, resource authorization, transactional idempotency and Kafka outbox/inbox behavior. Independently review database and failure invariants.
3. Extract the real React implementation into separate responsibilities. Preserve visual assets and user journeys; improve request cleanup, authentication state, component tests and accessible behavior.
4. Integrate an isolated local Compose environment and host hot reload. Run original acceptance, additional negative paths, persistent restart and broker-outage/dedup drills. Capture fresh screenshots at desktop/mobile.
5. Prepare AWS dev Terraform, mock/static validation and current prices; implement immutable GitHub Actions delivery and quality gates. AWS execution remains pending the account-specific saved plan and approval.
6. Produce linked interview explanations, Jira import, requirement traceability, AI review records and an honest release manifest. Independent critics compare implementation/evidence against reference behavior and documentation. Repair identified gaps until acceptance wins.

Architect review checkpoints: capability/data ownership, authentication compromise, outbox duplicate handling, migration rollback, environment isolation and IAM/secret boundaries. Local read-only inspection and reversible implementation are authorized. No cloud apply is scheduled. External account/repository configuration may remain pending without preventing local verification.
