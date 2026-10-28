---
title: "ECS networking, workload identity, and secrets"
topic: "ECS networking, workload identity, and secrets"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 54 · ECS networking, workload identity, and secrets

**Prerequisites:** 53 plus IAM and private connectivity from 46–49.

[Previous: 53](53-ecs-fargate-tasks-and-services.md) · [Next: 55](55-ecs-scaling-and-deployment-strategies.md) · [Study path](../README.md)

**Implementation boundary:** ECS task roles, execution roles, task ENIs, and ECS secret injection are absent from the existing Compose-on-EC2 root. Its actual host role must not be presented as an existing ECS role.

An elastic network interface (ENI) gives a Fargate task its network presence. An execution role grants the ECS/Fargate runtime permissions used to prepare the task, such as image pulls, log delivery, or configured secret injection. A task role supplies credentials to application code making AWS API calls. These identities operate at different lifecycle stages. A secret ARN names protected data; it is not the secret value, and possession of the ARN alone does not authorize retrieval.

## 1. Trace task startup as several independent requests

Start at scheduling and interface attachment, then image authorization and download, log initialization, secret retrieval, and process startup. Each request has a caller, destination, network path, and policy requirement. A private task may need several supported endpoints or an approved outbound path. An execution-role allow cannot repair missing DNS or routing. Likewise, working DNS and TLS cannot override a denied read. This decomposition makes a pre-start failure actionable.

## 2. Give the runtime a narrowly scoped execution role

Map registry pulls, log writes, and injected-secret reads to the execution role. Scope supported actions to relevant repositories, log streams, secrets, and keys; document action-specific exceptions such as authorization-token APIs. A customer-managed encrypted secret may also need appropriate KMS decrypt permission and key-policy authorization. Avoid granting business-data writes to this role merely because it is already attached to the task definition; application requests belong to the task role.

## 3. Give application code its own task role

If a catalog process needs object reads, assign the intended object permission to its task role. A different capability may need no AWS API access at all. SDK credential providers can obtain task credentials without embedding long-lived keys. Temporary credentials still require least privilege and safe handling. One shared image can run under different task roles. Never infer a task’s application permissions from the execution role’s ability to pull the image successfully.

## 4. Choose secret retrieval and rotation behavior

ECS can inject a referenced secret value at startup. This avoids hardcoded plaintext in task definitions, but the value exists in the process environment and must not be printed in diagnostics. Running tasks do not automatically refresh an injected secret after rotation; replacement or an application retrieval strategy is required. Runtime retrieval can support refresh but adds SDK, caching, permissions, and failure behavior. Choose an explicit approach and document old/new credential overlap.

## 5. Restrict traffic and interactive debugging

A future service SG should accept the application port from its intended entry SG and reach only required downstream destinations. Database authorization remains separate. ECS Exec is an administrative capability needing explicit IAM, connectivity, audit, and operational policy; it should not be a substitute for adequate logs. Avoid creating a debugging workflow that reveals environment secrets. Treat task-local shell inspection as sensitive access even when there is no SSH port or EC2 host administration.

## Source or illustrative example

**New illustrative identity matrix:** runtime → execution role → ECR pull/log write/startup secret; inquiries process → task role → only required AWS business APIs; operator → separate administrative role → controlled debugging. **Actual source anchor:** [host IAM policy](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/main.tf) supplies EC2 host operations today. Moving that policy wholesale into both ECS roles would preserve unnecessary coupling rather than establish the proposed separation.

## Safe exercise

Run a local permissions-owner classification:

```sh
python3 - <<'PY'
owners = {'image-pull':'execution', 'startup-secret':'execution',
          'application-s3-read':'task', 'operator-debug':'operator'}
for operation, role in owners.items():
    print(operation, '=>', role)
assert owners['application-s3-read'] != owners['image-pull']
PY
```

Expected outcome: four labeled operations and a passing separation assertion. Extend the table with IAM action, resource, KMS need, network destination, and rotation behavior. Do not add real secret values. Explain what changes if application code retrieves its own secret instead of using startup injection.

## Failure diagnosis

If the application never starts, inspect execution-role permissions and startup connectivity first. If it starts but an SDK call gets AccessDenied, inspect the task role and actual credential source. If rotation succeeds but tasks still use an old password, distinguish secret version changes from process refresh. If logs reveal values, repair logging and handle exposure through the authorized incident process; simply moving the value into Secrets Manager does not remove copies already emitted.

## Recall and answers

### Which role authorizes an application S3 request?

The task role used by application code, subject to the other applicable policies.

### Does injected secret rotation update existing process environments?

No. Running tasks need replacement or an explicitly implemented refresh/retrieval mechanism.

## Mastery check

Draw startup and runtime requests with distinct identities and network paths. Diagnose one execution-role denial and one task-role denial. Present a rotation timeline showing both service credentials and running consumers, with no real credentials in the learning artifact.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [Task execution IAM role](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html)
- [Task IAM role](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html)
- [Secrets Manager injection](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/secrets-envvar-secrets-manager.html)
- [Fargate networking](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-networking.html)
