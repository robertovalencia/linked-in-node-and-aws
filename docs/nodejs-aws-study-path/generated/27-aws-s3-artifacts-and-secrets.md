---
title: "S3 release objects, runtime secrets and state boundaries"
topic: "S3 release objects, runtime secrets and state boundaries"
last_researched: 2026-10-26
source_commit: 9bb88515f14067feb23611c6851c03ca8fbc89b6
---

# 27 · S3 release objects, runtime secrets and state boundaries

**Prerequisites:** 22 and 26; file permissions and JSON.

[Previous: 26](26-aws-docker-and-ecr.md) · [Next: 28](28-aws-data-and-messaging-decisions.md) · [AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md)

## 1. Distinguish the two S3 responsibilities

Bootstrap creates a protected bucket for Terraform state. The dev root creates a separate versioned bucket for release bundles. A bundle contains deployment scripts/configuration and a manifest; state maps Terraform addresses to infrastructure. Deleting either has different consequences. Neither bucket is a database backup simply because versioning is enabled.

## 2. Follow object access and versioning

The dev bucket blocks public access, enables encryption/versioning and denies insecure transport. The host policy reads only `releases/*`; the release identity writes that prefix. S3 versioning retains previous object versions, while an ordinary delete can leave versions/delete markers. The dev bucket's `force_destroy=true` deliberately permits data removal on approved teardown. That is different from the bootstrap bucket's `prevent_destroy` protection.

## 3. Keep secret values out of Terraform inputs

Terraform creates Secrets Manager metadata, not a secret-value resource in this design. A separate authorized step supplies fresh AWS-only runtime JSON. The host fetches it into a restricted environment file. Consequently these values do not enter Terraform state through secret resources here; do not generalize that Terraform always hides secrets. Adding a secret value as a managed argument could persist it in state even if marked sensitive.

## 4. Trace the trust boundary to the process

The remote script sets `umask 077`, validates required hex values, writes `.env`, and removes its temporary JSON. Root/SSM operators can still read the host's environment material. Logs, CLI arguments and screenshots must not contain the values. The Node request handlers consume environment configuration; they do not retrieve Secrets Manager values on each login.

## 5. Understand rotation as coordinated state change

Changing the secret JSON does not change passwords already stored by PostgreSQL. Existing roles need coordinated ALTER ROLE, secret update and application restart. Fresh volume initialization and existing-volume rotation are different paths. Rotating a shared JWT signing key can also invalidate existing user sessions. Treat rotation as an integration procedure, not a single API call.

## Walk the real project

[infra/aws-dev/main.tf · lines 42–45](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L42-L45)

```hcl
resource "aws_secretsmanager_secret" "runtime" {
  name                    = "${local.name}/runtime"
  recovery_window_in_days = 7
}
```

[scripts/aws-remote-deploy.sh · lines 4–14](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/scripts/aws-remote-deploy.sh#L4-L14)

```bash
umask 077
release_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$release_dir"
exec 9>/opt/marketplace/deploy.lock
flock -n 9 || { echo 'Another deployment is running'; exit 1; }
secret_arn=$(jq -er .secret_arn manifest.json)
region=$(jq -er .region manifest.json)
registry=$(jq -er .backend manifest.json | cut -d/ -f1)
trap 'rm -f "$release_dir/secret.json"' EXIT
aws secretsmanager get-secret-value --region "$region" --secret-id "$secret_arn" --query SecretString --output text >secret.json
python3 - <<'PY'
```

Open the host policy and the remote deployment script side by side. Identify who may read the secret ARN, where values are written, which permissions restrict the file and when temporary material is removed. Then distinguish secret metadata, stored value, process environment and application logs.

## Practice step by step

1. Make a four-row inventory: Terraform state, release bundle, runtime secret, database data. Name owner, storage, read path and cleanup behavior.
2. Read the remote script; mark secret-bearing variables without printing any real values.
3. Design a hypothetical password-rotation checklist including existing database roles and app restart.
4. Explain why an encrypted/versioned bucket still requires restricted access and retention policy.

**Expected evidence:** A storage/secret inventory and rotation plan tied to actual scripts, with no secret values copied into study notes.

## Check your understanding

### Is `secret_arn` a password?

No. It identifies a secret; access to its value requires authorization. The ARN still supplies environment context and should be handled deliberately.

### Does deleting the dev stack remove the bootstrap state bucket?

No. They belong to separate Terraform roots/states and use different destruction protections.

Do not mark this lesson complete until you can show the evidence and explain the result without reading the answer. Record your attempt and remaining question in your personal study notes; generated lessons are not personal progress records.

## References

Code excerpts are pinned to the inspected project revision `9bb8851`. They describe source, not proof that AWS resources were deployed. Official documentation was checked on 2026-10-26; verify account policies and selected tool versions before a real deployment.

- [S3 versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)
- [Secrets Manager practices](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- [Terraform S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3)
