---
title: "EC2, AMIs, EBS, metadata and bootstrap"
topic: "EC2, AMIs, EBS, metadata and bootstrap"
last_researched: 2026-10-26
source_commit: 9bb88515f14067feb23611c6851c03ca8fbc89b6
---

# 25 · EC2, AMIs, EBS, metadata and bootstrap

**Prerequisites:** 23–24; basic Linux services and Docker volumes.

[Previous: 24](24-aws-security-groups-and-ssm.md) · [Next: 26](26-aws-docker-and-ecr.md) · [AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md)

## 1. Read a machine definition as several decisions

An AMI provides the operating-system image. Instance type defines compute/memory characteristics. An instance profile supplies AWS identity. The network interface joins a subnet/security group. The root block device stores the operating system and, here, Docker data. Those settings are independent even though Terraform combines them in one resource.

The project resolves an Amazon Linux2023 x86_64 AMI from SSM Parameter Store. Its release builds target linux/amd64. Choosing an Arm instance without rebuilding compatible images would change a real compatibility assumption. The `m7i-flex.large` selection and account eligibility in old cost notes must be rechecked before a future launch.

## 2. Follow persistent data to its physical lifetime

The encrypted 40 GiB gp3 root disk contains PostgreSQL and Kafka Docker volumes. Restarting a container or rebooting the host is different from terminating/replacing the instance. `delete_on_termination=true` means termination removes this disk. Named volumes do not provide protection against losing their underlying host storage. Plan backups/restores before changing an instance in a real environment.

## 3. Explain metadata choices precisely

The instance requires IMDSv2 tokens and uses response hop limit 1. Host deployment scripts obtain the role through host credentials. Containers are not intended to consume host credentials. If future container AWS SDK calls need metadata, investigate workload identity and hop-limit behavior; do not increase the value reflexively and expose a powerful host role.

## 4. Bootstrap is preparation, not release verification

User data installs Docker, jq, Python and the AWS CLI, enables services and places a pinned Compose wrapper. It does not prove databases migrated, APIs became ready or all 48 business checks passed. Terraform uses `user_data_replace_on_change=true`; editing bootstrap can therefore replace the host and its disposable data. Learn to read the plan before assuming a script edit is harmless.

## 5. Inspect CPU-credit logic without overgeneralizing

The dynamic credit block is present only for T-family choices and selects standard mode. The default non-T instance omits that field. An unsupported CPU-credit option is an API error, not evidence that Terraform cannot create EC2. Evaluate sizing with actual memory/CPU/I/O measurements rather than the number of service containers.

## Walk the real project

[infra/aws-dev/main.tf · lines 107–118](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L107-L118)

```hcl
  metadata_options {
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }
  root_block_device {
    volume_type           = "gp3"
    volume_size           = 40
    encrypted             = true
    delete_on_termination = true
  }
  # CPU-credit options apply only to burstable T instances. Non-T families
  # such as m7i-flex must omit the API field entirely.
```

[infra/aws-dev/user-data.sh · lines 1–7](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/user-data.sh#L1-L7)

```bash
#!/bin/bash
set -euo pipefail
dnf install -y docker jq python3 awscli-2
systemctl enable --now docker amazon-ssm-agent
install -d -m 0700 /opt/marketplace/releases
# Compose is vendored in release bundles from the validated CLI container in CI.
# The host uses that pinned container against its Docker socket, avoiding curl|sh.
```

Locate AMI lookup, `instance_type`, instance profile, credit block and user-data replacement flag in the full resource. For each setting, write whether a change may affect identity, compatibility, cost, connectivity or data lifetime. These are the questions to ask during a Terraform plan review.

## Practice step by step

1. Trace PostgreSQL data from Compose volume to the instance root disk.
2. Make a table for container restart, EC2 reboot, instance replacement and termination; predict which data survives.
3. Read `user-data.sh` without executing it locally. Explain each package/service operation and the pinned Docker CLI wrapper.
4. Explain why a planned user-data replacement requires a data-retention decision.

**Expected evidence:** A data-lifetime table, bootstrap explanation and a replacement review note identifying potential data loss.

## Check your understanding

### Does encrypted EBS mean the data is backed up?

No. Encryption protects stored bytes; backup and restore address loss/recovery. This source does not implement automated database backups.

### Is successful EC2 creation proof of a working application?

No. Infrastructure, bootstrap, process readiness and business acceptance are separate checkpoints.

Do not mark this lesson complete until you can show the evidence and explain the result without reading the answer. Record your attempt and remaining question in your personal study notes; generated lessons are not personal progress records.

## References

Code excerpts are pinned to the inspected project revision `9bb8851`. They describe source, not proof that AWS resources were deployed. Official documentation was checked on 2026-10-26; verify account policies and selected tool versions before a real deployment.

- [Instance metadata and IMDSv2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)
- [EC2 user data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)
- [EBS volumes](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volumes.html)
