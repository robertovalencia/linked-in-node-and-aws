# ECS preparation evidence — 27 October 2026

This directory contains fresh local runtime/test reports and sanitized read-only planning summaries. No cloud deployment, publication or recovery is claimed. Existing migration evidence remains in its original locations.

- [Verification manifest](verification-manifest.json): exact source/evidence SHA256 values and executed counts.
- [Saved-plan/cost ledger](staging-plan-cost-review.json): current Ohio local-backend 108-create preview, binary/JSON hashes and 12 deterministic cases; the real plan/state are ignored, never in Git.
- [Negative controls](plan-negative-controls.json): unsafe rule/data/bypass rejection; private saved-plan fixture, not provisioning.
- [PostgreSQL](postgres-tls-ownership-replay.json), [Kafka](kafka-tls-scram-acl.json), [nginx DNS](frontend-dns.json), [API acceptance](local-acceptance.json), [browser](browser-smoke.json), [dependency recovery](failure-drill.json).
- [Source check](source-check.txt), [unit tests](unit-tests.txt), [build](build.txt), [ECS mocks](terraform-mocks.txt), [certificate mocks](certificate-mocks.txt), [release contracts](release-contracts.txt).
- [IAM draft warnings](iam-analysis-summary.json): three generated policies with 12 wildcard warnings; not attached or approved.

The source-commit field identifies the checked-out commit when each report was generated. Dirty-source reports also bind individual file hashes; final plan binding and hosted verification are tracked in the publication record. Neither a hash nor a passing mock grants approval to apply. Read [the selected environment guide](../../aws-ecs-dev.md) and [results](../../results.md) for the remaining gates.
