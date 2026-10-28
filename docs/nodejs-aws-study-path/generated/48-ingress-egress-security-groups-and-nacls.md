---
title: "Ingress, egress, security groups, and network ACLs"
topic: "Ingress, egress, security groups, and network ACLs"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 48 · Ingress, egress, security groups, and network ACLs

**Prerequisites:** 47 and 46; distinguish routing from authorization.

[Previous: 47](47-vpc-cidr-ipv6-and-subnet-design.md) · [Next: 49](49-private-connectivity-nat-and-endpoints.md) · [Study path](../README.md)

**Implementation boundary:** The project security group deliberately has zero ingress and broad IPv4 egress. The ALB/application/database trust chain below is a proposed public-service architecture, not an edit to that current control.

Ingress is traffic entering a resource or boundary; egress is traffic leaving it. A security group (SG) applies stateful allow rules to associated network interfaces. A network ACL (NACL) applies ordered, stateless allow and deny rules at a subnet boundary. Stateful means return traffic for an allowed flow is tracked. Stateless means the return packets must independently match permitted rules. Neither mechanism authenticates a browser user or checks ownership of an inquiry.

## 1. Trace one connection in both directions

Write client address, destination address, protocol, destination port, and ephemeral client port. Find the route and every filtering boundary. A request may pass an inbound server rule while its response is blocked by a stateless ACL. Security-group state tracking usually permits responses to an allowed flow without a separate mirror rule. Use precise packet direction rather than saying “open the port,” which hides the source and scope of the permission.

## 2. Build a proposed SG trust chain

For a future ALB design, the ALB SG permits intended client HTTPS ingress; the application SG permits its application port from the ALB SG; the database SG permits PostgreSQL only from the application SG. Allow the corresponding outbound paths from their sources. SG references identify permitted interfaces in supported relationships, not end-user identity and not transitive trust. Adding public application ingress would expand exposure; it is justified only by the proposed entry design.

## 3. Account for health and management traffic

A load balancer’s health check may use a different path or port from normal requests. Include that documented path in the proposed ALB-to-target allowance. Keep administrative access separate: the current project uses SSM, not SSH or browser ingress to the host. A health endpoint should disclose little and answer predictably, but hiding it behind application login can prevent the load balancer from assessing readiness. Choose controls according to the actual caller.

## 4. Use NACLs with explicit return-path reasoning

NACL rules are evaluated by rule number and stop at the first match. Custom restrictive ACLs can accidentally block ephemeral ports, cross-tier responses, or service endpoints. Model both inbound and outbound rules and both address families when applicable. Treat subnet ACLs as an additional boundary with an operational cost in complexity. Copying SG rules into a NACL is not a safe translation because SGs and NACLs have different state and rule semantics.

## 5. Keep network permission separate from service authorization

A reachable PostgreSQL socket still requires database authentication and grants. A reachable S3 endpoint still requires IAM and resource-policy permission. A permitted HTTPS request still requires JWT validation and business authorization in the API. Document these layers separately in the traffic matrix. During Terraform review, inspect source, protocol, ports, IPv4/IPv6 scope, and replacement consequences; a shorter resource block is not evidence of a narrower security boundary.

## Source or illustrative example

**New illustrative traffic matrix, not implemented:** client → ALB TCP 443; ALB SG → app SG TCP 8183; app SG → database SG TCP 5432. Health checks follow the selected target port. The [actual no-ingress SG](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/main.tf) supports SSM-oriented development access. It does not implement this trust chain and should not be described as insecure merely because it has no ALB.

## Safe exercise

Inspect declared rules without AWS access:

```sh
rg -n -A 17 'resource "aws_security_group" "dev"' infra/aws-dev/main.tf
```

Expected outcome: an empty ingress list and an all-protocol IPv4 egress rule in this pinned source. Draw a separate proposed traffic matrix with source SG, destination SG, port, purpose, and authentication layer. Then insert a deny-all outbound NACL rule into the drawing and identify which return packets fail. This is a reasoning exercise; do not edit infrastructure.

## Failure diagnosis

A timeout suggests checking DNS, routes, ACLs, SGs, listener binding, and service health. A TCP refusal usually means the destination responded but no suitable listener accepted the connection. An HTTP 401 or PostgreSQL authentication error means some network path succeeded; investigate application credentials rather than widening SGs. If health checks fail but manual requests succeed, compare source identity, path, Host header, port, protocol, and expected status code from the actual checker.

## Recall and answers

### Do SG rules need a response-port mirror for every allowed request?

State tracking generally permits return traffic; stateless NACLs need independent return-path allowances.

### Can the database SG trust every request forwarded through the ALB automatically?

No. SG references are not transitive; the database needs the intended application source and its own database authorization.

## Mastery check

Defend the proposed ALB-to-app-to-database matrix and a separate management path. Diagnose one return-path failure and one authentication failure without recommending broad ingress. Clearly distinguish the proposed public-service design from the current zero-ingress host.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [Security group rules](https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html)
- [Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)
- [ALB health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)
