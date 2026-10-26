---
title: "Release delivery: GitHub verification, OIDC and exact identity"
topic: "Release delivery: GitHub verification, OIDC and exact identity"
last_researched: 2026-10-26
source_commit: 9bb88515f14067feb23611c6851c03ca8fbc89b6
---

# 40 · Release delivery: GitHub verification, OIDC and exact identity

**Prerequisites:** Terraform32–39 and AWS22,26–27.

[Previous: 39](39-terraform-validation-and-mocked-tests.md) · [Next: 41](41-aws-ssm-deployment-and-rollback.md) · [AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md)

## 1. Separate infrastructure provisioning from application release

Terraform provisions the dev resource graph. Release tooling verifies/builds/publishes images and changes the running application. The GitHub deploy workflow contains no Terraform apply job. Its deploy input defaults false. An AWS role assumption is not proof that infrastructure has been approved or that business behavior passed.

## 2. Trace the selected local-login path

The local helper requires clean committed main from the exact independent repository, a successful verification-only `Deploy AWS dev` workflow_dispatch run for that SHA, the expected verification job and skipped deploy job, full 48-check acceptance and a Sonar result bound to that source. A generic successful workflow from another commit is rejected. Ordinary Verify success and this release-specific gate are different evidence contracts.

## 3. Follow identity into artifacts

The helper compares AWS account and region with initialized Terraform outputs, checks namespace/state, builds linux/amd64 images, resolves immutable ECR digests and runs the pinned vulnerability scanner. It then invokes the deployment path with a manifest. This makes the claim “this verified source produced these deployed artifacts” inspectable rather than inferred from a tag name.

## 4. Understand optional GitHub OIDC

If separately enabled, GitHub requests a short-lived identity token and assumes the restricted deploy role. Trust pins audience and `repo:OWNER/REPO:environment:dev`; the workflow uses the protected dev environment. Environment branch/reviewer protection complements trust. `id-token:write` permits obtaining the token, not arbitrary AWS actions; the role's permission policy still limits operations.

## 5. Preserve failure evidence

Failing authentication, wrong account, dirty checkout, missing gate evidence or a failed scan should stop release before deployment. Do not bypass those conditions to complete a tutorial. Study the local fixture tests: they exercise invalid contexts without making live AWS changes. A passed fixture is a contract test, not a published cloud image.

## Walk the real project

[scripts/aws-release-local.mjs · lines 58–64](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/scripts/aws-release-local.mjs#L58-L64)

```javascript
  requireThat(String(run.id) === runId && run.path === '.github/workflows/deploy-dev.yml' && run.head_repository?.full_name === repository && run.head_sha === sha && run.head_branch === 'main' && run.event === 'workflow_dispatch' && run.status === 'completed' && run.conclusion === 'success', 'Require a successful Deploy AWS dev workflow_dispatch run for this exact repository/main/SHA');
  const jobs = json('gh', ['api', `repos/${repository}/actions/runs/${runId}/jobs?filter=latest`]);
  await saved('github-jobs.json', jobs);
  const verification = jobs.jobs?.filter(job => job.name === 'verify');
  const deployment = jobs.jobs?.filter(job => job.name === 'deploy');
  requireThat(verification?.length === 1 && verification[0].conclusion === 'success' && deployment?.length === 1 && deployment[0].conclusion === 'skipped', 'Require successful verification-only CI with the AWS deploy job skipped');
  const artifactDir = join(evidence, 'verification');
```

[.github/workflows/deploy-dev.yml · lines 5–15](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/.github/workflows/deploy-dev.yml#L5-L15)

```yaml
      deploy:
        description: 'Deploy to AWS after verification (false runs verification only)'
        type: boolean
        default: false
        required: true
permissions:
  contents: read
concurrency:
  group: aws-dev-release
  cancel-in-progress: false
jobs:
```

Read `validateAcceptance`, `validateSonar`, the source/account checks and the deploy job condition in context. Compare selected local credentials with optional OIDC. Both paths require explicit authorization for the real environment; neither is a reason to store permanent AWS keys in GitHub or a browser bundle.

## Practice step by step

1. Draw infrastructure approval → source verification → artifact publication → scan → manifest → SSM → business acceptance.
2. Label which gates run locally, in GitHub and on the host.
3. Run only the existing local release contract tests if dependencies are installed; inspect a negative exact-SHA case.
4. Explain why OIDC subject restrictions and protected-environment rules solve different parts of authorization.

**Expected evidence:** A release gate diagram and a negative-case explanation showing how an unrelated successful run is rejected.

## Check your understanding

### Is `Verify` success alone the selected local release helper's required run?

No. The helper explicitly requires the successful verification-only deployment workflow for the exact repository/main/SHA and its artifact contract.

### Does OIDC remove the need for IAM permissions?

No. It changes how a session is obtained; scoped AWS authorization still applies afterward.

Do not mark this lesson complete until you can show the evidence and explain the result without reading the answer. Record your attempt and remaining question in your personal study notes; generated lessons are not personal progress records.

## References

Code excerpts are pinned to the inspected project revision `9bb8851`. They describe source, not proof that AWS resources were deployed. Official documentation was checked on 2026-10-26; verify account policies and selected tool versions before a real deployment.

- [GitHub OIDC with AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)
- [Temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html)
- [ECR tag immutability](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-tag-mutability.html)
