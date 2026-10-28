---
title: "Private connectivity, NAT, and VPC endpoints"
topic: "Private connectivity, NAT, and VPC endpoints"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 49 · Private connectivity, NAT, and VPC endpoints

**Prerequisites:** 47–48; IAM evaluation from 46.

[Previous: 48](48-ingress-egress-security-groups-and-nacls.md) · [Next: 50](50-dns-route53-acm-and-tls.md) · [Study path](../README.md)

**Implementation boundary:** The existing host reaches outside its VPC through an internet-gateway route and public addressing. NAT gateways, interface endpoints, gateway endpoints, VPN, and inter-VPC designs are broader proposed topics.

Private addressing does not automatically provide access to AWS APIs. A private application may need image downloads, log delivery, secret retrieval, and external partner calls before it can become healthy. NAT translates an outbound connection’s address. A VPC endpoint provides a service-specific connectivity path; interface endpoints use private network interfaces through AWS PrivateLink, while gateway endpoints for supported services use route-table entries. Connectivity and API authorization remain separate controls.

## 1. Inventory dependencies before selecting connectivity

Write every outbound destination and the component initiating the call. Include container startup dependencies, not just business requests: a task may require ECR API and image layers, S3, Secrets Manager, and CloudWatch Logs. Group destinations into AWS service APIs, private enterprise services, and public internet sites. This makes missing dependencies visible and avoids assuming that one endpoint supplies all AWS access or all traffic needed by a runtime.

## 2. Model the NAT path completely

A conventional public NAT gateway uses a public subnet, Elastic IP, and route to an internet gateway. Private workloads route their intended outbound IPv4 destinations to the NAT gateway. NAT does not allow arbitrary unsolicited inbound internet sessions and does not authenticate the external destination. Consider Availability Zone failure domains and cross-zone dependencies when sketching a resilient path. This lesson makes no cost comparison or claim that the project should replace its current routing.

## 3. Understand endpoint routing and DNS

An interface endpoint creates private interfaces and uses security groups; private DNS can make a normal service hostname resolve to the endpoint when configured correctly. A gateway endpoint is associated with route tables for its supported service. Inspect resolver settings, endpoint subnets, SGs, and route associations. The application’s hostname matters: a request sent to an unsupported endpoint hostname or address family may bypass the assumed private path or fail entirely.

## 4. Layer endpoint policy with IAM and resource policy

An endpoint policy limits what may pass through the endpoint; it does not grant an application permission that its service authorization lacks. Resource policies can constrain access to intended networks or endpoints, but incorrect explicit-deny conditions can block operators and AWS service integrations. Test exception logic before adopting it. Keep a documented recovery path for policy mistakes and avoid copying condition operators without checking absent-key and service-principal behavior.

## 5. Distinguish other private-network building blocks

VPC peering connects eligible VPCs directly but is not general transitive routing. Transit Gateway can provide a routed hub with explicit attachments and route tables. VPN and Direct Connect address hybrid connectivity with different operational characteristics. PrivateLink exposes particular services rather than merging entire network address spaces. Choose the primitive that matches the required communication relationship, and document both forward and return routing plus overlapping-address constraints.

## Source or illustrative example

**New illustrative startup dependency graph:** private Fargate task → ECR authorization/API; image-layer path → S3; logging → CloudWatch Logs; injected runtime secret → Secrets Manager. This is an architecture exercise, not current project configuration. The exact required endpoints depend on platform, Region, image registry, feature use, and DNS settings; verify the Fargate documentation before proposing a concrete design.

## Safe exercise

Run a local dependency completeness check:

```sh
python3 - <<'PY'
required = {'registry-api', 'image-layers', 'logs', 'secrets'}
proposed = {'registry-api', 'image-layers', 'logs'}
print('missing:', ', '.join(sorted(required-proposed)))
PY
```

Expected outcome: `missing: secrets`. Replace the labels with a written dependency table containing protocol, initiating role, hostname, and planned path. Explain why adding an IAM allow cannot repair this missing route, and why adding a route cannot repair a denied secret read.

## Failure diagnosis

A task stuck before application logs appear may be failing image pull, secret retrieval, or log initialization. Check startup-stage errors, DNS answers, endpoint SGs, and service-specific policies before changing application code. If some AWS APIs work privately while one fails, confirm that endpoint service’s availability and private DNS behavior. If all external HTTPS fails after a route edit, inspect the NAT and internet-gateway paths and return controls. Do not assume endpoint presence proves actual use.

## Recall and answers

### Does a VPC endpoint replace IAM authorization?

No. Network access and service authorization are separate requirements.

### Why inventory image-layer access separately from registry API access?

Authentication and image manifest access can succeed while the actual image-layer download path remains unavailable.

## Mastery check

Draw a private workload’s startup and business-call dependency paths. Explain one DNS failure, one endpoint-policy denial, and one missing public-egress route. State which destinations genuinely need internet access and which can use supported private paths, without changing this environment.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)
- [AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [Fargate networking](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-networking.html)
