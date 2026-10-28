---
title: "Local network-security reasoning lab"
topic: "Local network-security reasoning lab"
last_researched: 2026-10-27
source_labels: Professional core curriculum; Official documentation; Explicit illustrative examples
---

# 81 · Local network-security reasoning lab

**Prerequisites:** VPC routing, SG ingress/egress, NACLs and ALB/application/database boundaries.

[Previous lesson](80-staged-modernization-and-traceability.md) · [Next lesson](82-terraform-advanced-local-lab.md) · [Full syllabus](44-cloud-complete-syllabus-and-mastery-map.md)

## 1. State exactly what the simulator models

The accompanying standard-library Python lab evaluates a small teaching model of new TCP connections, required ingress/egress permissions and established reply state. It uses synthetic addresses and group names. It does not contact AWS, create a VPC, run containers or emulate the complete EC2 security-group implementation.

Route reachability and NACL permission are explicit inputs in the model, not discoveries from an account. That distinction is intentional: a group rule cannot create a missing network route, and an allowed route does not authorize traffic. Passing the local model is not proof the future deployed network behaves the same way.

## 2. Read the proposed trust chain

The example allows an approved documentation-range client to reach the ALB group on HTTPS 443. ALB may reach the app group on its teaching listener port. App may reach the database group on PostgreSQL 5432. These are new illustrative rules for a possible architecture, not edits to the current no-ingress Terraform.

The database rule names the app group as its allowed peer. That does not mean the ALB inherits database access merely because ALB can reach app. SG references express the allowed source group at the destination boundary; they are not transitive trust relationships.

## 3. Follow both sides of a new connection

For a managed source group, the lab checks source egress and destination ingress. For the synthetic external client, it checks the intended destination rule and explicit external path assumptions. A connection denied by either required permission is not accepted. Ports are part of the flow: allowing HTTPS does not allow SSH or database access.

Use least reachability as an engineering question, not a slogan. The absence of a needed ALB-to-app rule prevents a legitimate journey; an overly broad database source admits an unintended path. A useful test suite proves both kinds of behavior.

## 4. Understand established response traffic

The model records an accepted connection and permits its matching reverse response. This illustrates stateful security-group behavior. It does not add an all-ports outbound rule to a database simply to send a reply. An unsolicited connection from the database to an app ephemeral port is different and remains denied in the example.

NACLs are stateless and their return-path requirements are a separate topic. The lab’s NACL input only demonstrates that another layer can veto reachability; it does not calculate ordered NACL rule numbers or every ephemeral-port range. Explain that limit instead of presenting the simulator as an AWS firewall engine.

## 5. Relate the exercise to the current baseline

The [existing no-ingress Terraform baseline](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/main.tf) does not need these ALB/application/database group rules while its browser entry is SSM and all application/data processes share one host’s Docker network. Adding the teaching rules would change the architecture. The deployment owner must first assess requirements, costs, migration and exact exposure; this lab never applies them.

## 6. Turn predictions into evidence

Before running, predict which of the listed positive and negative flows should pass. Afterward inspect the explicit test names, then change only a copied teaching input and explain the resulting denial/allowance. Restore the secure teaching model and rerun. The runner verifies that its source input did not change during checks.

## Example and current-project boundary

**New local lab:** [rules](../labs/network-security/rules.json), [runner](../labs/network-security/run.py) and [walkthrough](../labs/network-security/README.md).

Run from the repository root:

```sh
python3 docs/nodejs-aws-study-path/labs/network-security/run.py
```

Only local JSON is read and local assertions run. No AWS credentials, SDK, endpoint or paid API is used.

## Practice with observable evidence

1. Draw approved-client → ALB → app → database with protocol/port labels.
2. Predict direct client-to-app, direct client-to-database and ALB-to-database outcomes.
3. Run the lab; compare every PASS name with your prediction, including established reply and missing-route/NACL veto cases.
4. Explain two checks a real AWS deployment would still require: actual network reachability/SG attachment and actual authenticated encrypted application/database behavior.

**Expected evidence:** the runner’s PASS transcript plus an explicit statement of what its teaching model does not verify.

## Recall and interview defense

### Why does ALB-to-app permission not imply ALB-to-database permission?

The database’s allowed source identity is checked independently; group references do not create transitive trust.

### Is a matching SG rule enough to guarantee connectivity?

No. Routing, NACLs, listeners, addressing, health, TLS and authentication can still prevent a successful operation.

## Mastery gate

Explain the mechanism without reading, show the stated evidence, identify a failure case and say which facts were tested locally versus merely proposed for AWS. Keep personal notes in your existing protected progress area. Learning a service does not require deploying it in the portfolio.

## References

Official sources checked on 2026-10-27. These teach mechanisms; any account-specific cost comparison, service selection or provisioning belongs to the deployment chat and requires its own current evidence.

- [Security group rules](https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html)
- [Security group connection tracking](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-connection-tracking.html)
- [Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)
