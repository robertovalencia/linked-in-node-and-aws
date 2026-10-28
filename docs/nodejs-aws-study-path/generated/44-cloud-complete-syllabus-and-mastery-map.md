---
title: "Cloud curriculum: syllabus and mastery map"
topic: "Cloud curriculum: syllabus and mastery map"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 44 · Cloud curriculum: syllabus and mastery map

**Prerequisites:** Lessons 20–43 and the existing local Terraform lab.

[Previous: 43](43-aws-terraform-capstone-and-interview.md) · [Next: 45](45-aws-account-governance-and-landing-zones.md) · [Study path](../README.md)

**Implementation boundary:** This lesson deliberately replaces the earlier repository-limited learning scope with a broader professional core. It does not replace the project infrastructure. The current source describes a single EC2 development host; most managed-service designs in lessons 45–83 are proposals for study.

A curriculum is a sequence of capabilities with evidence, not a list of product logos. The professional target is to explain a requirement, select an appropriate design, predict its failure modes, review its Terraform representation, and describe how an operator would verify it. “Complete” here means complete coverage of the finite core below, followed by explicit electives. It does not mean learning every AWS service or receiving proof of production experience from reading documentation. The [coverage matrix](../cloud-coverage.json) maps this expansion to individual lessons.

## 1. Establish the starting architecture

Read the pinned architecture and infrastructure before proposing changes. A Region is an AWS geographic deployment area; an Availability Zone is an isolated location within one Region. An account is an identity, governance, and resource boundary. The existing development host runs the capability containers and their data services together. Explain that shared failure boundary first. A valid learning comparison starts with actual constraints rather than silently treating an EC2 Compose project as an ECS deployment.

## 2. Learn identity and network foundations before managed services

Study account governance and IAM in 45–46, then addressing, traffic controls, connectivity, DNS, TLS, load balancing, and caching in 47–52. The dependency matters: a task that cannot pull an image may have a network problem, an IAM problem, or both. Define the principal, destination, route, transport, and authorization for every connection. These concepts transfer across AWS services and make troubleshooting more reliable than memorizing console screens.

## 3. Advance through compute, data, and event systems

Lessons 53–56 cover ECS, task identity, deployment behavior, EC2 scaling, and EKS comparisons. Lessons 57–63 cover relational recovery, caching and DynamoDB, Kafka, messaging, serverless, storage, and key management. A managed service changes the division of operational work; it does not remove schema design, retry safety, application authorization, or restore verification. For each service, state what AWS operates and what your team still owns.

## 4. Connect operations to Terraform engineering

Continue with lessons 64–83 for security detection, observability, recovery, production delivery, and the deeper Terraform sequence. Infrastructure as code describes intended resources; state links resource addresses to remote objects; a plan proposes changes. Review is the bridge between source and effects. Study modules, provider behavior, state operations, policy, testing, imports, drift, and migrations as engineering decisions. Read each lesson prerequisite rather than assuming the numeric order is the only possible path.

## 5. Grade evidence and choose electives intentionally

Use four evidence levels: define the concept, reason through a scenario, reproduce a safe local exercise, and verify an authorized environment. This course supplies the first three where possible; it does not claim the fourth. Build electives around a job requirement: analytics and Redshift, data engineering and Glue, AI with Bedrock, hybrid networking, advanced Kubernetes, or specialized databases. Record the missing capability and its acceptance evidence before adding another service to the syllabus.

## Source or illustrative example

**Actual source anchor:** [architecture](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/docs/architecture.md) and [AWS development root](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/main.tf) establish the current design. **New illustrative target:** “An inquiry remains recoverable after losing one application host.” That requirement creates questions about external data, replicas, backups, idempotency, and recovery evidence. Merely changing the compute service cannot answer all of them.

## Safe exercise

Run this read-only source inspection from the repository root:

```sh
rg -n 'resource "aws_(instance|ecs_service|db_instance|lb|vpc)"' infra
```

Expected outcome: identify the EC2/VPC definitions and accurately report whether each searched managed service exists in source. Absence from this search is a prompt to inspect modules and other resource forms, not universal proof. Then write a three-column study record: capability, lesson, evidence still needed. Pick one network incident and one data-loss incident and map each across at least three lessons.

## Failure diagnosis

If a learner can recite service names but cannot trace a request, the gap is mechanism: return to 47–54. If a design survives a process restart but loses acknowledged data after replacement, revisit 57, 59, and 62. If a Terraform example is mistaken for a deployed resource, separate source evidence, local validation, and runtime evidence in the study record. If progress stalls on too many electives, choose one target role and one concrete outcome before expanding scope.

## Recall and answers

### Does finishing every lesson prove a production deployment?

No. Reading, local execution, source review, and live operational verification are different forms of evidence.

### What makes the map professionally useful?

It joins requirements, mechanisms, failure reasoning, and reviewable evidence, while exposing electives and unverified assumptions.

## Mastery check

Present a one-page capability map and defend the next three lessons you will study. Identify two existing project mechanisms, two proposed services, and one elective outside the core. Do not mark the map mastered until a reviewer can ask “what fails next?” and you can point to the relevant lesson and evidence.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [AWS Organizations overview](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html)


## Concept-level checklist for the complete core path

Explain each concept, complete its exercise, and record the remaining live evidence. Important absent project features remain part of the path.

| Lesson | Concepts to master |
|---|---|
| [20 · cloud-roadmap-and-lab](20-cloud-roadmap-and-lab.md) | Learning gates, evidence boundaries, current implementation versus new examples |
| [21 · aws-accounts-regions-and-cli](21-aws-accounts-regions-and-cli.md) | Accounts, Regions and AZs, ARNs, CLI profiles, effective configuration |
| [22 · aws-iam-roles-and-policies](22-aws-iam-roles-and-policies.md) | Principals, trust policies, permissions, instance profiles, STS, application roles |
| [23 · aws-vpc-subnets-and-routing](23-aws-vpc-subnets-and-routing.md) | CIDR, subnets, route tables, IGW, public addressing, Docker versus VPC DNS |
| [24 · aws-security-groups-and-ssm](24-aws-security-groups-and-ssm.md) | Stateful SGs, no-ingress baseline, SSM agent/operator identity, port forwarding |
| [25 · aws-ec2-ebs-and-bootstrap](25-aws-ec2-ebs-and-bootstrap.md) | AMI, CPU architecture, EBS data lifetime, IMDSv2, user data, replacement |
| [26 · aws-docker-and-ecr](26-aws-docker-and-ecr.md) | Images versus containers, ECR push/pull, tags versus digests, scanning, retention |
| [27 · aws-s3-artifacts-and-secrets](27-aws-s3-artifacts-and-secrets.md) | Release objects versus state, versioning, runtime secrets, file permissions, rotation |
| [28 · aws-data-and-messaging-decisions](28-aws-data-and-messaging-decisions.md) | Service-owned relational data, outbox/inbox, managed database/broker migration |
| [29 · aws-observability-and-incidents](29-aws-observability-and-incidents.md) | Health versus business acceptance, logs/metrics/traces, incident hypothesis |
| [30 · aws-costs-and-cleanup](30-aws-costs-and-cleanup.md) | Cost quantity inventory, dated assumptions, cleanup versus stop, retained versions |
| [31 · aws-production-design-tradeoffs](31-aws-production-design-tradeoffs.md) | Requirements, availability, stateful scaling, production trust, recovery tradeoffs |
| [32 · terraform-hcl-and-first-local-lab](32-terraform-hcl-and-first-local-lab.md) | HCL blocks, resource addresses, declarative lifecycle, local built-in provider lab |
| [33 · terraform-providers-versions-and-init](33-terraform-providers-versions-and-init.md) | Provider installation, version constraints, dependency lock, init versus backend |
| [34 · terraform-inputs-locals-and-outputs](34-terraform-inputs-locals-and-outputs.md) | Variable types, validation, locals, outputs, input precedence, null |
| [35 · terraform-graph-loops-and-modules](35-terraform-graph-loops-and-modules.md) | Dependency graph, implicit/explicit dependencies, count, for_each, module boundaries |
| [36 · terraform-state-locking-and-bootstrap](36-terraform-state-locking-and-bootstrap.md) | Resource state, S3 backend, native lockfile, bootstrap root, sensitive state |
| [37 · terraform-plan-apply-and-drift](37-terraform-plan-apply-and-drift.md) | Saved plans, detailed exit codes, apply, drift, refresh, partial failure |
| [38 · terraform-lifecycle-import-and-refactoring](38-terraform-lifecycle-import-and-refactoring.md) | Lifecycle replacement, prevent_destroy limits, import, moved addresses |
| [39 · terraform-validation-and-mocked-tests](39-terraform-validation-and-mocked-tests.md) | fmt, validate, terraform test, mocked provider limits, meaningful assertions |
| [40 · aws-release-pipeline-and-oidc](40-aws-release-pipeline-and-oidc.md) | Exact-source gates, CI versus release, OIDC trust, scopes, source-to-digest chain |
| [41 · aws-ssm-deployment-and-rollback](41-aws-ssm-deployment-and-rollback.md) | SSM invocation identity, readiness versus acceptance, rollout lock, rollback/data limits |
| [42 · aws-terraform-troubleshooting-workbook](42-aws-terraform-troubleshooting-workbook.md) | Diagnostic layers, backend versus provider errors, policy denial, safe repair |
| [43 · aws-terraform-capstone-and-interview](43-aws-terraform-capstone-and-interview.md) | Five-minute defense, evidence packet, current topology, honest deployment limits |
| [44 · cloud-complete-syllabus-and-mastery-map](44-cloud-complete-syllabus-and-mastery-map.md) | Full syllabus, dependency order, concept evidence, core versus specialist scope |
| [45 · aws-account-governance-and-landing-zones](45-aws-account-governance-and-landing-zones.md) | Shared responsibility, account isolation, Organizations, OUs, SCPs, landing zones, quotas |
| [46 · iam-policy-evaluation-and-federation](46-iam-policy-evaluation-and-federation.md) | IAM policy evaluation, resource/session permissions, federation, boundaries, ABAC, PassRole |
| [47 · vpc-cidr-ipv6-and-subnet-design](47-vpc-cidr-ipv6-and-subnet-design.md) | IPv4/IPv6, subnet sizing, AZ placement, route precedence, peering and hybrid awareness |
| [48 · ingress-egress-security-groups-and-nacls](48-ingress-egress-security-groups-and-nacls.md) | Ingress/egress, stateful SGs, stateless NACLs, ephemeral return ports, nontransitive references |
| [49 · private-connectivity-nat-and-endpoints](49-private-connectivity-nat-and-endpoints.md) | Private egress, NAT, gateway/interface endpoints, PrivateLink, private DNS, endpoint policies |
| [50 · dns-route53-acm-and-tls](50-dns-route53-acm-and-tls.md) | DNS delegation, Route53 records/aliases/routing, ACM, TLS handshake, certificate regions |
| [51 · alb-target-groups-and-health-checks](51-alb-target-groups-and-health-checks.md) | ALB listeners/rules, target groups, health checks, SG chain, TLS termination, draining |
| [52 · cloudfront-s3-origins-and-caching](52-cloudfront-s3-origins-and-caching.md) | CloudFront origins, OAC, cache keys/TTL/invalidation, security headers, TLS and private origins |
| [53 · ecs-fargate-tasks-and-services](53-ecs-fargate-tasks-and-services.md) | ECS cluster/task/service, Fargate versus EC2 capacity, task definitions, desired state |
| [54 · ecs-networking-identity-and-secrets](54-ecs-networking-identity-and-secrets.md) | Task versus execution roles, awsvpc, app/data SGs, secret injection, service discovery |
| [55 · ecs-scaling-and-deployment-strategies](55-ecs-scaling-and-deployment-strategies.md) | Autoscaling, capacity providers, rolling/blue-green/canary, circuit breaker, health and actions |
| [56 · ec2-autoscaling-and-eks-comparison](56-ec2-autoscaling-and-eks-comparison.md) | EC2 ASG, launch templates, instance refresh, Spot interruption, EKS control plane and RBAC |
| [57 · rds-postgresql-backups-and-failover](57-rds-postgresql-backups-and-failover.md) | RDS PostgreSQL, subnet groups, TLS, pools, backups/PITR, replicas/Multi-AZ, migrations |
| [58 · data-caching-and-dynamodb-design](58-data-caching-and-dynamodb-design.md) | DynamoDB access patterns, keys/indexes, conditional writes, consistency, cache invalidation/TTL |
| [59 · msk-kafka-security-and-operations](59-msk-kafka-security-and-operations.md) | MSK Kafka, partitions/groups, listener authentication, TLS, retention, lag, replay, migration |
| [60 · sqs-sns-eventbridge-and-workflows](60-sqs-sns-eventbridge-and-workflows.md) | SQS visibility/DLQ/idempotency, SNS fanout, EventBridge routing, Step Functions orchestration |
| [61 · lambda-apigateway-and-serverless-design](61-lambda-apigateway-and-serverless-design.md) | Lambda lifecycle/concurrency/retries, API Gateway auth/throttling, cold starts, tracing |
| [62 · s3-ebs-efs-storage-and-recovery](62-s3-ebs-efs-storage-and-recovery.md) | Object/block/file storage, S3 lifecycle/versioning, EBS snapshots, EFS access, consistency |
| [63 · kms-secrets-and-rotation](63-kms-secrets-and-rotation.md) | KMS envelope encryption, key and IAM policy, grants, secret rotation, state and key recovery |
| [64 · waf-shield-and-security-detection](64-waf-shield-and-security-detection.md) | WAF web ACL/rate rules, Shield layers, GuardDuty, Inspector, Security Hub, prevention/detection |
| [65 · cloudwatch-agent-logs-metrics-and-alarms](65-cloudwatch-agent-logs-metrics-and-alarms.md) | CloudWatch agent, host/task collection, metric dimensions/statistics, logs, metric alarms, missing data |
| [66 · cloudtrail-config-and-audit-evidence](66-cloudtrail-config-and-audit-evidence.md) | CloudTrail management/data events, Config history/rules, identity/outcome, audit retention |
| [67 · otel-tracing-slos-and-incidents](67-otel-tracing-slos-and-incidents.md) | OpenTelemetry spans/context, async links, sampling/privacy, SLIs/SLOs, error budget, incident RCA |
| [68 · disaster-recovery-and-resilience-testing](68-disaster-recovery-and-resilience-testing.md) | RTO/RPO, backup consistency, key recovery, restore testing, multi-AZ versus multi-region, fault drills |
| [69 · cloud-cost-allocation-and-optimization](69-cloud-cost-allocation-and-optimization.md) | Allocation/ownership, quantity/unit drivers, budgets versus caps, right-sizing, idle/residual costs |
| [70 · terraform-expressions-and-type-system](70-terraform-expressions-and-type-system.md) | Expressions/functions, collection transformations, optional/default/null, unknown values, templates |
| [71 · terraform-modules-and-contracts](71-terraform-modules-and-contracts.md) | Module contracts, root/child boundaries, source/version pinning, outputs, semantic compatibility |
| [72 · terraform-provider-aliases-and-environments](72-terraform-provider-aliases-and-environments.md) | Provider aliases, configuration_aliases, regions/accounts, environment state, workspace limits |
| [73 · terraform-remote-state-and-access-control](73-terraform-remote-state-and-access-control.md) | Backend authentication, restricted remote state, output exposure, locking, state splitting, encryption |
| [74 · terraform-sensitive-and-ephemeral-values](74-terraform-sensitive-and-ephemeral-values.md) | Sensitive redaction versus state, ephemeral values, write-only arguments, version/provider support |
| [75 · terraform-import-moves-and-provider-upgrades](75-terraform-import-moves-and-provider-upgrades.md) | Imports, moved/removed blocks, stable identity, address changes, provider upgrades and lockfiles |
| [76 · terraform-testing-and-policy-as-code](76-terraform-testing-and-policy-as-code.md) | Validation/pre/postconditions/checks, terraform test mocks versus apply, TFLint, OPA/Sentinel policy |
| [77 · terraform-team-ci-and-approval-workflows](77-terraform-team-ci-and-approval-workflows.md) | PR/fork safety, OIDC, protected plan artifacts, saved-plan approval, CI separation, drift scheduling |
| [78 · terraform-drift-recovery-and-state-surgery](78-terraform-drift-recovery-and-state-surgery.md) | Partial failure, refresh-only, backup/lineage, state repair, force-unlock ownership, recovery boundaries |
| [79 · cloud-threat-model-and-security-review](79-cloud-threat-model-and-security-review.md) | Assets/actors/trust boundaries, data/control plane, threat model, allowed/denied tests, break-glass |
| [80 · staged-modernization-and-traceability](80-staged-modernization-and-traceability.md) | Learning versus deployment scope, cost-first ownership, phased questions, coordination evidence |
| [81 · network-security-local-lab](81-network-security-local-lab.md) | Local network simulation, required/forbidden flows, reply state, route/NACL limits, no AWS proof |
| [82 · terraform-advanced-local-lab](82-terraform-advanced-local-lab.md) | Advanced local modules, filtered for_each, validations, address moves, test expectations, cleanup |
| [83 · professional-cloud-capstone-and-question-bank](83-professional-cloud-capstone-and-question-bank.md) | Architecture defense, random concept review, local evidence, requirements, limits and pending owner work |
