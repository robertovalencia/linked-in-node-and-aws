---
title: "KMS, Secrets Manager, and credential rotation"
topic: "KMS, Secrets Manager, and credential rotation"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 63 · KMS, Secrets Manager, and credential rotation

**Prerequisites:** 46, 54, and 62; encryption versus recovery.

[Previous: 62](62-s3-ebs-efs-storage-and-recovery.md) · [Next: 64](64-waf-shield-and-security-detection.md) · [Study path](../README.md)

**Implementation boundary:** The current root declares Secrets Manager secret metadata and encrypted storage, but does not declare a customer-managed KMS key or an automatic secret-rotation workflow. These additional mechanisms are proposed study topics.

AWS Key Management Service (KMS) manages cryptographic keys and permissions for supported cryptographic operations. Envelope encryption uses a data key for data and protects that data key under another key. Secrets Manager stores versioned secret material and can coordinate supported rotation mechanisms. A KMS key is not a password vault, and encrypting a password does not change the database credential itself. Rotation must update the authoritative service and its consumers through a controlled lifecycle.

## 1. Classify keys and secrets before choosing controls

A secret is a value such as a database password or API credential whose disclosure grants access. A KMS key controls cryptographic operations and has its own lifecycle. AWS owned, AWS managed, and customer managed keys have different control and policy responsibilities. Choose the required control deliberately rather than calling every encrypted resource “customer-key encrypted.” Current source uses an S3 AES256 setting and EBS encryption; those facts do not prove the existence of a customer-managed project KMS key.

## 2. Review KMS authorization as its own surface

Key policies, IAM policies, grants, and service integration behavior can influence key use. A general S3 or Secrets Manager allow may still fail when the caller lacks the required decrypt authorization for a customer-managed key. Scope permissions to intended roles and uses where supported, and review encryption-context conditions carefully. A key administrator need not be an unrestricted data reader. Cross-account use and recovery require both access layers and key availability to be designed explicitly.

## 3. Keep secret values out of infrastructure evidence

Terraform can manage a secret container separately from secret material. A value marked sensitive is hidden in some UI output but can still exist in state, provider requests, or saved artifacts. Avoid putting real values in HCL, plan examples, shell history, or course evidence. Reference the protected secret by identifier and define the authorized injection/update workflow separately. The project’s secret metadata declaration is not proof that a real value was set, safely retrieved, or rotated.

## 4. Design rotation as a state transition

Rotation updates credentials in the database or external service and the stored secret, with validation and safe promotion. Depending on the integration, a managed mechanism or a rotation function may coordinate the work. Consider pending/current versions, old/new overlap, failure recovery, and whether consumers cache credentials. ECS startup-injected secrets do not refresh existing process environments automatically. An application that retrieves secrets at runtime needs bounded caching, refresh, and degraded-mode behavior without revealing values in errors.

## 5. Protect key and secret lifecycle during recovery

Deleting or disabling a necessary key can make otherwise intact encrypted backups unusable. Rotating KMS key material differs from rotating a database password and does not automatically rewrite every previously encrypted object or change application credentials. Secret deletion recovery windows and backup retention should align with operational needs. Record who can schedule destructive lifecycle changes, how they are reviewed, and what evidence confirms consumers work after rotation. A successful rotation API response is not sufficient business acceptance.

## Source or illustrative example

**Actual source anchor:** [runtime secret metadata and storage encryption declarations](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/main.tf). **New illustrative rotation timeline:** create a pending database credential, set it in the database, test authentication, promote it, refresh consumers, and retire the old credential only after the chosen safe-overlap strategy. This is a conceptual sequence; exact rotation implementation depends on the service and is not deployed here.

## Safe exercise

Run a local secret-version state simulation without real credentials:

```sh
python3 - <<'PY'
versions={'v1':{'current':True,'tested':True}, 'v2':{'current':False,'tested':False}}
versions['v2']['tested']=True
assert versions['v2']['tested']
versions['v1']['current']=False
versions['v2']['current']=True
print([v for v, state in versions.items() if state['current']])
PY
```

Expected outcome: `['v2']`. These labels contain no secret material and do not simulate database or consumer updates. Add those missing actors to a rotation diagram. Explain what happens if the secret version is promoted but an ECS task still holds the previous startup-injected value.

## Failure diagnosis

A decrypt denial requires checking the actual key, key policy/grant, caller, service path, and relevant context conditions. A new password failing only in older tasks suggests consumer refresh behavior; failure everywhere may indicate the authoritative service was never updated or the wrong secret key/version was selected. A rotation stuck at a pending stage requires investigating validation and recovery, not blindly promoting it. A missing KMS key during restore is a recovery dependency failure even when the backup files are present.

## Recall and answers

### Does rotating a KMS key rotate a PostgreSQL password?

No. Cryptographic key lifecycle and application credential lifecycle are distinct.

### Does Terraform sensitive marking keep a secret out of state?

No. It controls some display behavior; state and artifacts still require protection and deliberate secret handling.

## Mastery check

Explain envelope encryption, key authorization, secret versioning, and consumer refresh as separate mechanisms. Produce a rotation failure timeline and a recovery dependency map. Identify what the current source actually declares and what would still need implementation and authorized verification.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [KMS key concepts](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html)
- [Secrets Manager rotation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)
- [ECS injected secret behavior](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/secrets-envvar-secrets-manager.html)
- [Terraform sensitive data and state](https://developer.hashicorp.com/terraform/language/manage-sensitive-data)
