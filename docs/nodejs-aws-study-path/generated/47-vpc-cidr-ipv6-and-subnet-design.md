---
title: "VPC addressing, IPv6, and subnet design"
topic: "VPC addressing, IPv6, and subnet design"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 47 · VPC addressing, IPv6, and subnet design

**Prerequisites:** 46; basic IP addresses and TCP connections.

[Previous: 46](46-iam-policy-evaluation-and-federation.md) · [Next: 48](48-ingress-egress-security-groups-and-nacls.md) · [Study path](../README.md)

**Implementation boundary:** The actual root declares VPC 10.84.0.0/16 and one IPv4 subnet 10.84.1.0/24. Multiple Availability Zones and IPv6 below are proposed design exercises.

A VPC is a logically isolated regional network. A subnet is an address range within one Availability Zone. CIDR notation combines a network address and prefix length: a smaller prefix number describes a larger address range. A route table chooses a next hop for a destination, using the most specific matching route. None of these objects grants application permission. Address planning determines whether future connectivity and service placement remain possible without disruptive renumbering.

## 1. Allocate non-overlapping ranges before naming tiers

List networks that might connect: other accounts, corporate sites, VPN clients, and partner ranges. Overlapping address space can prevent straightforward routing between them. Divide the chosen VPC range into repeatable allocations for Availability Zones and workload tiers, leaving expansion space. Avoid deriving the range only from today’s small host count. A subnet needs capacity for service-created network interfaces and replacement overlap during deployments, not just long-lived application instances.

## 2. Associate each subnet with an Availability Zone

An Availability Zone is a failure domain, not a security tier. A proposed resilient design might repeat public edge, private application, and isolated data subnets across zones. Write which service creates interfaces in each tier and how application traffic crosses zones. A picture with three subnets in one zone does not provide zone redundancy. The repository’s single subnet is useful for its bounded development purpose but should not be described as a multi-zone architecture.

## 3. Classify public and private by routes

A public subnet has a route to an internet gateway. For ordinary IPv4 internet communication, a workload also needs an appropriate public address and permissive traffic controls; merely residing there does not make it reachable. Private application subnets can use NAT for selected outbound IPv4 needs. Isolated data subnets omit general internet routes. Inspect explicit and main route-table associations because a subnet name such as `private-a` does not enforce privacy.

## 4. Plan IPv6 as a distinct traffic path

IPv6 has separate addresses, routes, DNS records, and security rules. A dual-stack design must review both families, including outbound-only patterns using an egress-only internet gateway where appropriate. Do not assume IPv4 NAT or an IPv4-only SG restriction controls IPv6 traffic. Check the selected managed service’s current IPv6 support before designing an IPv6-only tier. The curriculum teaches the boundary; it does not assert this project has IPv6 configured.

## 5. Represent intent with Terraform and review consequences

Use stable subnet keys such as tier and zone identifiers when later building modules, rather than relying on accidental list order. Validate that subnet CIDRs belong to the VPC range and do not overlap. Address-space edits can replace resources and disconnect dependent services. Review those consequences before implementation. Keep the address worksheet separate from evidence of deployed routes; a syntactically valid CIDR is only one part of a working network.

## Source or illustrative example

**Actual source anchor:** [VPC, subnet, gateway, and route declarations](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/main.tf). **New illustrative layout:** reserve 10.96.0.0/16 for a future environment, then allocate 10.96.0.0/24 and 10.96.1.0/24 to different logical tiers. These values are local arithmetic inputs, not approved AWS network allocations.

## Safe exercise

Use Python’s standard library locally:

```sh
python3 - <<'PY'
import ipaddress
vpc = ipaddress.ip_network('10.96.0.0/16')
subnets = [ipaddress.ip_network(x) for x in ['10.96.0.0/24','10.96.1.0/24']]
assert all(s.subnet_of(vpc) for s in subnets)
assert not subnets[0].overlaps(subnets[1])
print([s.num_addresses for s in subnets])
PY
```

Expected outcome: `[256, 256]` raw addresses, not the number AWS makes assignable. Add a deliberately overlapping range and observe the assertion fail. Explain why range arithmetic cannot verify route associations, service quotas, or interface consumption.

## Failure diagnosis

If a service cannot allocate an interface, check free subnet addresses and placement constraints before assuming CPU capacity is the issue. If peered or VPN-connected networks fail, inspect overlapping CIDRs and both return routes. If IPv4 works while a client fails intermittently, inspect AAAA resolution and the IPv6 path independently. If a supposedly private host receives public traffic, verify the route table, addresses, and both address-family security rules rather than trusting a subnet label.

## Recall and answers

### Does a public subnet force a host to accept internet traffic?

No. Route, addressing, security rules, and the listening application all matter.

### Why reserve addresses for deployments?

Old and replacement interfaces can coexist, so steady-state capacity is not the deployment peak.

## Mastery check

Produce an address plan with two zones, three logical tiers, growth room, and no overlaps. Trace separate IPv4 and IPv6 outbound paths. Explain which parts differ from the actual one-subnet development root and which future service requirements still need verification.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [Configure a VPC](https://docs.aws.amazon.com/vpc/latest/userguide/configure-your-vpc.html)
- [Fargate networking](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-networking.html)
- [NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)
