---
title: "From this dev stack to a production design"
topic: "From this dev stack to a production design"
last_researched: 2026-10-26
source_commit: 9bb88515f14067feb23611c6851c03ca8fbc89b6
---

# 31 · From this dev stack to a production design

**Prerequisites:** All AWS foundation lessons 21–30.

[Previous: 30](30-aws-costs-and-cleanup.md) · [Next: 32](32-terraform-hcl-and-first-local-lab.md) · [AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md)

## 1. Begin with requirements rather than a service shopping list

Write expected traffic, availability, recovery-time/recovery-point objectives, data classification, public access needs and operational ownership. RTO is the time objective for restoring service; RPO is the acceptable data-loss window. The current single-host demo supplies neither a production SLO nor tested disaster recovery. A proposed architecture must justify its extra complexity against concrete goals.

## 2. Separate compute scaling from state scaling

Four processes can share an image without scaling safely as one unit. Stateless API replicas need compatible routing, session/auth behavior and independent readiness. PostgreSQL/Kafka need deliberately designed durability, connections and partitions. Adding containers to another host does not move the existing volumes or provide failover. An ECS/Fargate proposal also requires task identity, networking, discovery, resource limits and deployment policy.

## 3. Design public entry and trust boundaries

A production browser entry might introduce DNS, TLS certificates, an HTTPS load balancer or static delivery through object storage/CDN. Those resources are absent here. Decide origin protection, authentication, CORS, secure cookie/token policy and rate limiting rather than assuming TLS fixes application authorization. Separate production secrets and environments from synthetic demo seeds.

## 4. Design state and recovery together

Evaluate managed PostgreSQL backups/failover and managed Kafka against application semantics, recovery drills and cost. Plan schema compatibility for rolling deployment and rollback. Encryption does not demonstrate restore capability. A multi-zone diagram is insufficient unless applications tolerate failover and recovery is practiced with measured evidence.

## 5. Keep Terraform boundaries deliberate

Use separate environment state/credentials and narrowly scoped deployment identities. Reusable modules may help repeat a stable pattern, but the current repository has two roots, not a reusable module catalog. Decide team ownership, blast radius and state dependencies before splitting files into modules. Preserve exact artifact identity and release evidence during any infrastructure redesign.

## Walk the real project

[docs/aws-dev.md · lines 5–8](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/docs/aws-dev.md#L5-L8)

```text
## Why one EC2 host

The four Node services, PostgreSQL, Kafka, and frontend run on one `m7i-flex.large` Amazon Linux 2023 x86_64 host (2 vCPU, 8 GiB RAM) in `us-east-2` for the selected 24-hour Free plan demonstration. Each service still owns a distinct database and role. A single host keeps a small dev environment explainable and avoids an ALB, NAT gateway, RDS, and managed Kafka baseline bill. ECS/Fargate plus RDS/MSK would improve service lifecycle and database resilience, but brings more infrastructure and a higher minimum bill. This deployment has no high availability, automated backups, or production SLO claim. Database and Kafka volumes live on the encrypted root disk: replacing/terminating the instance loses them. Snapshot/export before replacement.

```

[infra/aws-dev/main.tf · lines 100–107](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L100-L107)

```hcl
resource "aws_instance" "dev" {
  depends_on             = [aws_route_table_association.dev, aws_iam_role_policy.host, aws_iam_role_policy_attachment.ssm]
  ami                    = data.aws_ssm_parameter.ami.value
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.dev.id
  vpc_security_group_ids = [aws_security_group.dev.id]
  iam_instance_profile   = aws_iam_instance_profile.host.name
  metadata_options {
```

Use the real resource list as the baseline column of a before/after table. Every proposed new service must name the limitation it resolves, the new operational obligation, the cost driver and a test that would demonstrate the improvement. Do not relabel the existing stack as production-ready.

## Practice step by step

1. Choose hypothetical RTO/RPO and traffic goals; mark them as assumptions.
2. Draw a proposed multi-zone design and a smaller intermediate improvement.
3. Compare current EC2 Compose with the proposal across availability, delivery, data recovery, network trust and cost.
4. List three migration risks and the evidence required before retiring the old setup.

**Expected evidence:** Two labeled designs plus a tradeoff/validation table grounded in the existing code.

## Check your understanding

### Should every interview project use Kubernetes?

No. Explain the required capability and operational cost first. A smaller design can be appropriate when its limits are explicit.

### Can you claim the proposed managed services are implemented?

No. Point to the actual Terraform resources and describe extensions as design work. Honest scope is part of a defensible architecture explanation.

Do not mark this lesson complete until you can show the evidence and explain the result without reading the answer. Record your attempt and remaining question in your personal study notes; generated lessons are not personal progress records.

## References

Code excerpts are pinned to the inspected project revision `9bb8851`. They describe source, not proof that AWS resources were deployed. Official documentation was checked on 2026-10-26; verify account policies and selected tool versions before a real deployment.

- [AWS service overview](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html)
- [VPCs and subnets](https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html)
- [IAM roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
