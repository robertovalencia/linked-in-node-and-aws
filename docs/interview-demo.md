# Interview demonstration and questions

Use the [local setup](local-setup.md), then rehearse this 12–15 minute story. This is a portfolio laboratory, not a claim of production employment experience.

1. Browse anonymously. Filter by category, budget, availability and skill; compare two profiles and open experience/portfolio. Explain that records come from PostgreSQL through catalog APIs.
2. Log in as company. Submit an inquiry and show the actual response. Explain JWT verification, role checks and why request idempotency needs a database invariant under concurrency.
3. Log in as Ava. Edit the owned profile, refresh, inspect inquiry and accept. Return as company and show persisted acceptance. Demonstrate Leo cannot modify Ava's inquiry.
4. Show one inquiry/outbox transaction and its Kafka notification. Explain broker outage buffering and duplicate delivery; show the failure-drill evidence. Do not claim exactly-once delivery across PostgreSQL/Kafka.
5. Open `frontend/src` to follow route → hook → service → API. Compare the reference's single large file with separate components and explain stale requests and visible failures.
6. Show a backend test, frontend behavior test, the 48-check report, critic repair and CI/Sonar configuration. Distinguish locally executed gates from external gates pending account setup.
7. Open Terraform and explain EC2/SSM/ECR, secret/state separation and immutable deployment/rollback. Show the cost estimate and validation. State whether AWS was actually provisioned; demonstrate cloud runtime only after approval/execution.

| Question | Answer to practice |
|---|---|
| Why NestJS? | Structured modules, DI and controllers make framework boundaries familiar after Spring; business rules remain explicit. |
| Why four services? | Capability ownership and failure/release practice; a modular monolith would reduce MVP overhead. |
| What if two retries arrive simultaneously? | Client-scoped durable idempotency and transaction coordination, not browser disabled buttons or one process's memory. |
| What if Kafka is unavailable? | Inquiry/outbox commit persists intent; publisher retries after recovery; eventual notifications. |
| Can an old image roll back a migration? | No; use backward-compatible migrations and test restore separately. |
| Why not deploy to Kubernetes? | AWS dev uses one host for a small learning environment; EKS adds cost/operational demands. Explain the scale/availability tradeoff. |
| What did AI actually contribute? | Codex implementation and reviews under human requirements; adapted reference behavior/assets; percentage target not measured. |
| Where is traceability? | Requirement ID → Jira import → implementation/test → commit → workflow/artifact digest → deployment/release record. |

Deeper explanations: [architecture](architecture.md), [Java-to-NestJS](interview-topics/java-to-nestjs.md), [data/security](interview-topics/data-security.md), [frontend](interview-topics/frontend.md), [AWS](aws-dev.md), [Azure](azure-mapping.md), and [AI workflow](ai-development.md).
