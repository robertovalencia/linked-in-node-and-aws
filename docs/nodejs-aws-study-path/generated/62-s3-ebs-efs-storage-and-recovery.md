---
title: "S3, EBS, EFS, and recoverable storage"
topic: "S3, EBS, EFS, and recoverable storage"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 62 · S3, EBS, EFS, and recoverable storage

**Prerequisites:** 57; host replacement and container storage from 25 and 53.

[Previous: 61](61-lambda-apigateway-and-serverless-design.md) · [Next: 63](63-kms-secrets-and-rotation.md) · [Study path](../README.md)

**Implementation boundary:** The actual development root uses an encrypted EC2 root EBS volume and S3 release artifacts. EFS, independent application-data backups, and managed recovery designs below are proposals.

Object storage addresses objects by key through an API; block storage supplies a disk-like device; file storage exposes a shared filesystem interface. Amazon S3, EBS, and EFS represent these three models. Their APIs, sharing behavior, failure boundaries, and recovery procedures differ. Encryption protects stored data against certain disclosure threats; redundancy improves resilience to certain failures; a recoverable backup provides an independently usable restoration path. None of those words alone proves application data can be restored correctly.

## 1. Match storage semantics to the workload

Use object semantics for artifacts, uploads, and immutable blobs when the application can use object APIs. Use block storage when software requires disk/filesystem behavior on its compute host. Shared file storage can support applications requiring a common filesystem, with permissions and locking behavior reviewed carefully. Do not treat S3 as an ordinary POSIX disk or EFS as a universal database replacement. Describe access pattern, concurrency, durability requirement, and expected recovery before selecting a service.

## 2. Trace the current project’s data lifetime

The project’s PostgreSQL and Kafka container volumes ultimately live on the EC2 host’s root disk. The root block device is encrypted and configured for deletion on termination. Rebooting a host differs from replacing or terminating it. Terraform bootstrap changes can trigger replacement through the declared user-data behavior. Named Docker volumes do not escape the disk’s lifetime. The S3 release bucket contains deployment artifacts, not an implemented backup of those business database volumes.

## 3. Design storage access at each layer

S3 uses IAM, bucket policy, public-access controls, and optional encryption-key policy. EBS attachment and snapshot access involve AWS permissions, while filesystem access inside the guest uses operating-system permissions. EFS uses network reachability, NFS behavior, access points where chosen, and supported IAM authorization controls. A filesystem being private does not replace application-user permissions. For EFS, mount-target SGs must permit the intended NFS flow from clients; an allowed AWS API call alone does not mount a filesystem.

## 4. Make backup consistency and retention explicit

A snapshot of a busy application may be crash-consistent rather than application-consistent unless coordinated with the application or engine. Database-aware backups and log recovery can provide different guarantees. S3 versioning keeps object versions but does not by itself establish independent protection against every deletion or compromise. Define retention, independent access, restoration keys, account/Region boundaries, and legal needs. Lifecycle expiration is a deletion policy, so review it against rollback and recovery requirements before implementation.

## 5. Verify restoration at the business boundary

A recovered disk or object is only an intermediate result. Validate filesystem integrity, database startup, schema, credentials, expected records, event positions, and the application’s read/write behavior. Recovery may require reconciling an event replay with restored database state. Record RPO and RTO as targets, then distinguish hypothetical durations from measured restores. A backup owned by an unavailable account or encrypted under a deleted key can be unusable even when its storage object still exists.

## Source or illustrative example

**Actual source anchor:** [root EBS deletion setting and versioned S3 release bucket](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/main.tf). **New illustrative recovery proposal:** database-aware backups stored under independently governed retention, plus restore validation in an isolated target. This proposal does not claim the project has those backups or that a restore drill has run.

## Safe exercise

Run a local artifact restore demonstration in a temporary directory:

```sh
python3 - <<'PY'
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib, shutil
with TemporaryDirectory() as directory:
    root=Path(directory)
    source=root/'record.txt'; source.write_text('study-record-v1')
    backup=root/'backup.txt'; shutil.copy2(source, backup)
    source.unlink(); shutil.copy2(backup, source)
    print(hashlib.sha256(source.read_bytes()).digest()==hashlib.sha256(backup.read_bytes()).digest())
PY
```

Expected outcome: `True`, followed by automatic removal of only the temporary exercise directory. This verifies local byte restoration, not PostgreSQL consistency, AWS backup durability, or business recovery. Add the checks needed before making each stronger claim.

## Failure diagnosis

If data survives a restart but disappears after replacement, inspect the actual storage lifetime and termination settings. An EFS mount timeout points toward DNS, routes, NFS port reachability, and mount targets; permission denied requires authorization and filesystem identity review. An S3 read denial may involve bucket policy, object ownership, or KMS, not just IAM. A restored database that starts with missing business effects needs reconciliation, not a premature “backup passed” label.

## Recall and answers

### Does an encrypted root disk prove a usable backup exists?

No. Encryption and independent recoverability are separate properties.

### Why is byte restoration weaker than application recovery?

The application also needs consistent data, compatible schema, credentials, and validated business behavior.

## Mastery check

Map every current data store to its physical lifetime and propose an independent recovery path. Compare object, block, and shared-file access without conflating them. Demonstrate the local byte restore and list the missing evidence for a real database recovery claim.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- [EBS volumes](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volumes.html)
- [Amazon EFS](https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html)
- [RDS backup and restore concepts](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_CommonTasks.BackupRestore.html)
- [EBS deletion on termination](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/preserving-volumes-on-termination.html)
- [EFS mount diagnosis](https://docs.aws.amazon.com/efs/latest/ug/troubleshooting-efs-mounting.html)
- [S3 access-denied diagnosis](https://docs.aws.amazon.com/AmazonS3/latest/userguide/troubleshoot-403-errors.html)
