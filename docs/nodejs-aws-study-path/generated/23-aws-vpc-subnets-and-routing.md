---
title: "Networking: CIDR, VPCs, subnets and route tables"
topic: "Networking: CIDR, VPCs, subnets and route tables"
last_researched: 2026-10-26
source_commit: 9bb88515f14067feb23611c6851c03ca8fbc89b6
---

# 23 · Networking: CIDR, VPCs, subnets and route tables

**Prerequisites:** 21 and the meaning of an IP address, port, TCP connection and DNS.

[Previous: 22](22-aws-iam-roles-and-policies.md) · [Next: 24](24-aws-security-groups-and-ssm.md) · [AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md)

## 1. Translate the network ranges

A CIDR describes an address range. The project VPC is `10.84.0.0/16`; its subnet is `10.84.1.0/24`, a smaller range inside it. These are private IPv4 ranges, not public URLs. AWS reserves addresses within subnets, so do not assume every mathematical address is assignable. The region/zone distinction matters because one subnet does not span multiple zones.

## 2. Trace route selection separately from permission

A route table says where matching destination traffic goes. The dev subnet is associated with a table whose `0.0.0.0/0` route targets an internet gateway. Public addressing and that route support outbound internet use. A security group separately decides permitted traffic; an internet route is not a permission to connect to the application.

## 3. Explain what “public subnet” means here

The selected design assigns public IPv4 and routes through an internet gateway. It remains a public subnet even though the instance accepts no security-group ingress. Calling it a private subnet because the app is inaccessible would hide the real architecture. There is no NAT gateway or VPC endpoint in this source. A proposed private-subnet design needs a deliberate path to SSM, ECR, S3 and package repositories.

## 4. Follow both networking layers

Within EC2, Compose service names such as `catalog` resolve on a Docker network. Those names are not VPC DNS records or public hostnames. nginx calls Node services through container networking, and Node calls PostgreSQL/Kafka internally. Browser JavaScript uses same-origin API paths through nginx, not `http://catalog:8182` from the laptop.

## 5. Diagnose path failures in order

Separate local browser routing, SSM tunnel, host loopback listener, container port mapping, Docker DNS, service readiness and database dependency. Avoid changing a VPC route when the actual fault is an unhealthy container. For outbound failures, check DNS, route/public address, security-group egress, host configuration and endpoint authorization.

## Walk the real project

[infra/aws-dev/main.tf · lines 8–19](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L8-L19)

```hcl
resource "aws_vpc" "dev" {
  cidr_block           = "10.84.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
}
resource "aws_subnet" "dev" {
  vpc_id                  = aws_vpc.dev.id
  cidr_block              = "10.84.1.0/24"
  map_public_ip_on_launch = true
}
resource "aws_internet_gateway" "dev" { vpc_id = aws_vpc.dev.id }
resource "aws_route_table" "dev" {
```

[infra/aws-dev/main.tf · lines 19–27](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L19-L27)

```hcl
resource "aws_route_table" "dev" {
  vpc_id = aws_vpc.dev.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.dev.id
  }
}
resource "aws_route_table_association" "dev" {
  subnet_id      = aws_subnet.dev.id
```

Follow every `vpc_id`, `subnet_id` and `route_table_id` reference. Terraform uses them as dependency edges. Mark the subnet, associated route table and gateway on paper before adding any security rule. This becomes the real example for the Terraform graph lesson 35.

## Practice step by step

1. Draw laptop, SSM service, EC2 public subnet, host loopback, frontend container, API containers and data containers.
2. Label VPC CIDR and subnet CIDR. Mark which names resolve only inside Docker.
3. Trace an outbound ECR image pull and an inbound browser session as separate arrows.
4. Explain why removing the default route can break bootstrap even though no inbound port is open.

**Expected evidence:** Two complete traffic traces and a correct explanation of public subnet versus publicly reachable application.

## Check your understanding

### Does `map_public_ip_on_launch=true` expose PostgreSQL?

It does not publish a Docker port or add ingress permission. Exposure requires a complete reachable path and a listener; inspect each layer.

### Why not add a NAT gateway immediately?

The current subnet uses an internet gateway directly. A NAT design belongs to a different topology with additional cost and routing requirements.

Do not mark this lesson complete until you can show the evidence and explain the result without reading the answer. Record your attempt and remaining question in your personal study notes; generated lessons are not personal progress records.

## References

Code excerpts are pinned to the inspected project revision `9bb8851`. They describe source, not proof that AWS resources were deployed. Official documentation was checked on 2026-10-26; verify account policies and selected tool versions before a real deployment.

- [VPCs and subnets](https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html)
- [VPC route tables](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html)
- [Security groups](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
