# AWS visual study guide

Use this guide alongside the [setup walkthrough](../walkthroughs/README.md) and [full concept map](../generated/44-cloud-complete-syllabus-and-mastery-map.md). A screenshot helps you recognize the tool; its explanation connects what you see to the architecture and source code.

## Start here

- [Actual Array of Sunshine project captures](04-project-console-captures.md): current project, certificate and resource views, clearly scoped and distinct from AWS examples.

- [Recognize AWS sign-in and identity](01-sign-in-and-identity.md): actual blank sign-in capture and the role-versus-user distinction.
- [Your IAM Set permissions screen](03-iam-user-permissions.md): understand Copy permissions, attached policies and the optional boundary.
- [Nine official service screenshots](02-console-service-examples.md): VPC, security groups, ECS, ECR, ALB, RDS, CloudWatch Logs, S3 and ACM.

The official example images are online links and require internet access even in the ZIP. They are not copies of your account or deployment evidence.

## How to study a screen

1. Read the **provenance**: your actual account, an official AWS example, or a local tool.
2. Check the account/Region and capture date. A resource list applies only to its selected scope.
3. Locate the named field, explain what it controls, then open the linked code.
4. Answer the recall question before moving to another screenshot.

Screenshots are observations, not instructions to create resources. Never submit a creation form simply to reproduce an image. Credentials, secret values, exact approved client addresses and unrelated browser content are excluded. Account-specific screens may be cropped to the relevant service content; captions explain any omitted context.

## What a screenshot can establish

An ACM detail screen can establish the certificate status visible at capture time. It cannot prove application HTTPS. An empty ECS list can show that no clusters match the current account/Region/filter, but not that the entire account has no infrastructure. A service creation form can explain fields while proving no deployment at all. An alarm listed in CloudWatch does not prove notifications are delivered.

Use [the deployment coordination record](../deployment-coordination.json) and [owner plan review](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/docs/aws-https-plan-review-2026-10-28.md) for the dated deployment status. This visual guide makes no AWS changes and does not replace cost or deployment approval.

## Console and infrastructure vocabulary

| What you see | What it means | What to inspect in source |
|---|---|---|
| Region selector | Geographic scope of most service pages | `provider "aws"` and `var.region` |
| Resource status | A service-specific lifecycle observation | Resource definition plus actual runtime checks |
| VPC/subnet | Address space and placement | CIDRs, routes, AZ choices |
| Security group rules | Permitted network traffic | Direction, peer, protocol and port |
| ECS cluster/task/service | Grouping, running unit and desired-count management | Task/service definitions, roles and networking |
| Target group health | Whether load-balancer checks succeed | Listener routing, target port and health path |
| Database endpoint | Where a client connects | Private reachability, role credentials and TLS verification |
| Log group/alarm | Telemetry destination and condition | Actual emission, retention, dimensions and delivery |
| ECR repository/image digest | Image storage and exact content identity | Reviewed source-to-digest manifest |
| S3 bucket/versioning | Object storage and historical versions | State backend, artifact and retention boundaries |

Read screenshot captions as small concept cards. The source remains authoritative for proposed configuration; actual console evidence remains authoritative only for the observations captured.
