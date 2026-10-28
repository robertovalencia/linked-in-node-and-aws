# 3 · AWS identity and cost-first decisions

[Previous: application flow](02-project-and-application-flow.md) · [Index](README.md) · [Next: Terraform setup](04-terraform-setup-and-plans.md)

This chapter explains the deployment owner's recorded process. It does not initiate a login, refresh prices or provision resources. Current cost analysis and account changes belong to “Create Node.js AWS LinkedIn project.”

## 1. An account, a Region and an identity answer different questions

An **account** contains the resources and billing boundary. A **Region** selects a geographic service location. A **principal** is the identity making a request. Correct Terraform source can still operate in the wrong place if effective credentials or Region differ from the reviewed values.

The project's recorded deployment planning uses Ohio, `us-east-2`. Its owner checked the account and certificate again on 28 October. Read the [account preflight receipt](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/docs/evidence/aws-https-plan-2026-10-28/account-preflight.json); it is a dated observation, not a perpetual guarantee.

## 2. A CLI profile is a name for configuration

A profile such as `marketplace-dev` selects credential/configuration sources. The selected [AWS setup runbook](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/docs/aws-dev.md) uses temporary CLI login rather than creating permanent access keys. That runbook contains the actual authentication steps; do not paste tokens or credentials into Markdown.

After a valid authorized login, the owner verifies the effective identity. This is a read-only example for that operator, not a requirement for local study:

```bash
export AWS_PROFILE=marketplace-dev
export AWS_REGION=us-east-2
aws sts get-caller-identity
```

Expected: an account identifier and caller ARN. It proves that request's identity, not permission to create every planned resource. If credentials expire, refresh the selected temporary login and repeat the identity check. Do not “fix” expiration by granting broader IAM permissions.

The CLI and Terraform must inherit the same intended credential environment. A profile flag supplied to only one command does not automatically constrain every later process. Immediately recheck identity before a separately approved apply.

## 3. Separate human, delivery and workload permissions

The operator prepares/reviews resources. A CI identity verifies or publishes an exact source revision. An ECS **execution role** supports tasks' platform operations; an application **task role** authorizes AWS calls made by application code. They have different jobs. The [official role explanation](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html) distinguishes these boundaries.

The source also contains optional OIDC setup. A Terraform definition is not evidence that a GitHub identity provider or protected environment is active. The 28 October bootstrap preview does not create OIDC. See [bootstrap source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/bootstrap/main.tf) and [toolchain setup](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/docs/toolchain.md).

## 4. Inventory before proposing a new service

The original EC2/SSM design and the prepared ECS design are separate alternatives in source. The owner checked actual account resources before planning. Grepping a repository proves only what source mentions; account inventory needs authorized service queries, with their scope recorded.

On 28 October, the owner reported the certificate issued/unused and no application infrastructure in queried scopes. That is narrower than “the entire account has no resources.” The [dated plan review](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/docs/aws-https-plan-review-2026-10-28.md) is the current recorded reference for this walkthrough.

## 5. Convert architecture into billable quantities

The process was: inventory the baseline → propose alternatives → identify meters → retrieve dated regional prices → calculate scenarios → review costs before apply. The [27 October comparison](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/docs/aws-cost-review-2026-10-27/README.md) explains EC2 versus ECS/RDS, NAT versus endpoints and optional MSK. The [28 October review](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/docs/aws-https-plan-review-2026-10-28.md) updates the selected HTTPS preview and assumptions.

A NAT gateway can have time and traffic charges. A load balancer has time/capacity dimensions. Storage can persist after a process stops. These are categories to inspect, not a new price quote. Read the linked itemized model before deciding whether the learning benefit justifies a service. MSK and WAF remain conceptual study topics even when not selected for this demo.

## 6. Treat credits, budgets and estimates honestly

A recorded credit balance does not prove every requested service is eligible, or every bill will be covered. A budget alert does not stop resource usage automatically. A 24-hour estimate depends on its quantities and duration; the 720-hour comparison is a stated scenario rather than a promise about a calendar invoice.

The owner has not started the billable demonstration clock. State retention and recovery exercises need explicit treatment. Reuse the cost model's quantities; do not add an already-allocated state cost again. This chapter deliberately links the owner's calculation instead of maintaining a competing estimate.

**Understanding check:** If STS succeeds but Terraform receives AccessDenied, what was proved and what was not? Why can a stopped or destroyed application still leave costs?
