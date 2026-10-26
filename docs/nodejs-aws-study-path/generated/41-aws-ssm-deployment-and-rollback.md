---
title: "Deployment on SSM: readiness, acceptance and rollback"
topic: "Deployment on SSM: readiness, acceptance and rollback"
last_researched: 2026-10-26
source_commit: 9bb88515f14067feb23611c6851c03ca8fbc89b6
---

# 41 · Deployment on SSM: readiness, acceptance and rollback

**Prerequisites:** 40,25,27 and database migration basics.

[Previous: 40](40-aws-release-pipeline-and-oidc.md) · [Next: 42](42-aws-terraform-troubleshooting-workbook.md) · [AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md)

## 1. Follow the bundle to the host

A release manifest identifies source SHA, image digests, region, secret ARN and artifacts. S3 holds the bundle; SSM Run Command invokes the host deployment. The host script runs as root and obtains only the runtime configuration it needs. It uses a nonblocking `flock` to reject a simultaneous rollout. That host lock differs from Terraform's state lock and GitHub's workflow concurrency group.

## 2. Separate process startup from acceptance

Compose starts exact digest images and waits for readiness. The script then runs the complete bundled acceptance suite. The deployment controller checks the exact SSM invocation output for 48 PASS and 0 FAIL. An SSM command being accepted or a container being Up is not sufficient. Preserve command ID, instance, SHA and acceptance report so evidence refers to one actual rollout.

## 3. Trace the commit point of a release

The source retains release directories and updates the current symlink after successful checks. Read the failure branch before assuming a rollout is atomic. External observers may see temporary interruption during replacement on a single host; the design is not blue/green high availability. A successful response only establishes the checks that actually ran.

## 4. Understand rollback limits

A failed release can restore prior images when a prior release exists. A first deployment has no prior known-good release. Keeping an old image does not undo destructive database migrations or recover deleted root-disk data. Use expand/contract schema changes compatible with both versions; verify backups/restores when data recovery is required.

## 5. Keep credentials and cleanup visible

The script validates secret values and digest syntax, uses restrictive permissions and removes temporary secret JSON. The environment file remains readable to authorized host root. Never paste it into an incident report. Do not use `down -v` during rollback: deleting volumes changes the data-recovery problem entirely.

## Walk the real project

[scripts/aws-remote-deploy.sh · lines 7–13](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/scripts/aws-remote-deploy.sh#L7-L13)

```bash
exec 9>/opt/marketplace/deploy.lock
flock -n 9 || { echo 'Another deployment is running'; exit 1; }
secret_arn=$(jq -er .secret_arn manifest.json)
region=$(jq -er .region manifest.json)
registry=$(jq -er .backend manifest.json | cut -d/ -f1)
trap 'rm -f "$release_dir/secret.json"' EXIT
aws secretsmanager get-secret-value --region "$region" --secret-id "$secret_arn" --query SecretString --output text >secret.json
```

[Actual rollback and release pointer · lines 56–65](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/scripts/aws-remote-deploy.sh#L56-L65)

```bash
if [[ "$healthy" != true ]]; then
  echo 'Health verification failed; restoring previous application images.'
  if [[ -n "$previous" && -f "$previous/compose.yaml" ]]; then
    cd "$previous"
    marketplace-compose -f compose.yaml up -d --wait --wait-timeout 180
    bash ./aws-smoke.sh
  fi
  exit 1
fi
ln -sfn "$release_dir" /opt/marketplace/current
```

Read the full remote script and find its healthy flag, acceptance execution, failed rollout branch and current symlink update. Then inspect `scripts/aws-deploy.sh` for how a specific SSM invocation is polled and evidence validated. These code paths describe prepared operations; source alone does not demonstrate a live rollout.

## Practice step by step

1. Write a rollout timeline with explicit readiness, business acceptance and symlink checkpoints.
2. For each checkpoint, predict what remains after failure and where evidence is stored.
3. Write a first-deploy failure response and a later-release rollback response separately.
4. Explain one schema change compatible with both app versions and one destructive change that images alone cannot reverse.

**Expected evidence:** A failure timeline and rollback plan naming the data compatibility limitation and exact SSM evidence identity.

## Check your understanding

### Are GitHub concurrency, host flock and Terraform locking the same lock?

No. They serialize different actors and state changes. Name which operation each protects.

### Does restoring an image restore the database?

No. Data recovery and schema compatibility require separate measures and tests.

Do not mark this lesson complete until you can show the evidence and explain the result without reading the answer. Record your attempt and remaining question in your personal study notes; generated lessons are not personal progress records.

## References

Code excerpts are pinned to the inspected project revision `9bb8851`. They describe source, not proof that AWS resources were deployed. Official documentation was checked on 2026-10-26; verify account policies and selected tool versions before a real deployment.

- [Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)
- [S3 versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)
- [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)
