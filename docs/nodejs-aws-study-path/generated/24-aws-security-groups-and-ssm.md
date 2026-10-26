---
title: "Security groups, SSM access and encrypted tunnels"
topic: "Security groups, SSM access and encrypted tunnels"
last_researched: 2026-10-26
source_commit: 9bb88515f14067feb23611c6851c03ca8fbc89b6
---

# 24 · Security groups, SSM access and encrypted tunnels

**Prerequisites:** 22–23: identities and network paths.

[Previous: 23](23-aws-vpc-subnets-and-routing.md) · [Next: 25](25-aws-ec2-ebs-and-bootstrap.md) · [AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md)

## 1. Read the actual ingress policy

The dev security group has `ingress=[]`: no SSH 22 and no HTTP 80 entry. Its outbound rule permits IPv4 egress, allowing package, registry and AWS endpoint access. Security groups are stateful; network ACLs and host firewalls are separate mechanisms. Do not conflate a security group with the route table or Docker port publication.

## 2. Understand SSM prerequisites

Session Manager needs an installed/running agent, suitable instance-role permissions, network connectivity to required AWS endpoints and operator session permissions. The laptop needs its CLI/plugin for the documented tunnel. The `AmazonSSMManagedInstanceCore` attachment supports the agent; it does not authorize every human to open a session.

## 3. Trace the browser tunnel exactly

The runbook forwards laptop port 8088 through SSM to host port 80. Compose binds frontend to `127.0.0.1:80:8180`; nginx listens in its container and forwards API requests. The public EC2 address is not the browser entry point. Closing the tunnel makes the laptop path unavailable even if containers remain healthy.

## 4. Separate session types and audit evidence

An interactive shell, Run Command deployment and a port-forwarding session serve different purposes and can need different permissions. CloudTrail can record API activity; do not claim it captures commands inside a tunneled connection. Port-forwarding session traffic is not available as normal Session Manager command-content logs. Audit the deployment's SSM command ID and acceptance output separately.

## 5. Repair without opening the perimeter

If the instance is not managed, inspect role/profile, agent readiness and endpoint reachability. If a tunnel opens but HTTP fails, inspect the loopback bind, container status and nginx routing. Adding public HTTP or SSH ingress changes the design and bypasses the diagnostic lesson.

## Walk the real project

[infra/aws-dev/main.tf · lines 30–41](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L30-L41)

```hcl
resource "aws_security_group" "dev" {
  name        = local.name
  description = "No ingress. SSM manages host and tunnels browser traffic."
  ingress     = []
  vpc_id      = aws_vpc.dev.id
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

[infra/aws-dev/compose.yaml · lines 98–104](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/compose.yaml#L98-L104)

```yaml
  frontend:
    image: ${FRONTEND_IMAGE:?immutable frontend digest required}
    restart: unless-stopped
    ports: [127.0.0.1:80:8180]
    depends_on: [identity, catalog, inquiries, notifications]
    logging: {driver: json-file, options: {max-size: 10m, max-file: '3'}}
volumes:
```

Compare these two controls: no VPC ingress and loopback-only host publication. Then find `AWS-StartPortForwardingSession` in the operating guide and trace remote 80 → frontend 8180. Neither control is replaced by the other.

## Practice step by step

1. Source-only: reproduce the tunnel command on paper and label target instance, remote port and local port.
2. Create a checklist for “instance missing from SSM” and another for “tunnel connected, browser fails.”
3. Optional only for an existing authorized instance: follow the runbook's `start-session` command; end the session when finished. Do not provision a machine for this exercise.
4. Explain how you would preserve an SSM command ID without recording secrets.

**Expected evidence:** A correct laptop 8088 → SSM → host 80 → container 8180 diagram and two ordered diagnostic checklists.

## Check your understanding

### Why can the browser work with no inbound SG rules?

The documented access is an authenticated SSM tunnel supported by agent connectivity, not a public TCP connection to the instance.

### Does session API logging prove every command or tunneled byte was recorded?

No. Distinguish API audit, command output and session-content logging capabilities before making an audit claim.

Do not mark this lesson complete until you can show the evidence and explain the result without reading the answer. Record your attempt and remaining question in your personal study notes; generated lessons are not personal progress records.

## References

Code excerpts are pinned to the inspected project revision `9bb8851`. They describe source, not proof that AWS resources were deployed. Official documentation was checked on 2026-10-26; verify account policies and selected tool versions before a real deployment.

- [Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)
- [Security groups](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
- [CloudTrail auditing](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html)
