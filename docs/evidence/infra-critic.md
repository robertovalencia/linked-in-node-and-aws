# Independent infrastructure critic

Assessment: **WIN for the required prepared AWS scope** after two concrete repairs. This does not certify an actual AWS deployment. This is a review of prepared AWS infrastructure, not a deployed AWS environment.

## Single biggest gap: rollback leaves fetched secret JSON

`scripts/aws-remote-deploy.sh` installs `trap 'rm -f secret.json' EXIT` in the new release directory, then changes directory to the previous release when verification fails. The trap runs relative to the previous directory. The failed release retains `secret.json`, containing all fetched Secrets Manager values. Although the directory and file have restrictive permissions and `.env` is intentionally retained, this contradicts the script's cleanup contract and creates an unnecessary additional secret copy on the failure path.

Repair verified: the root uses an absolute cleanup target based on `release_dir` and installs the trap before fetching. Re-executed success and failed-acceptance/rollback fixtures both pass (2/2), including JSON cleanup, mode0600, prior-image recreation and `current` promotion behavior. The failed original is preserved in `infra-remote-orchestration-before-repair.json`.

Reproduction: `infra-remote-orchestration.json` uses a scratch copy of the actual remote deploy script with only `/opt/marketplace` replaced by a fixture directory. AWS, Docker, Compose, flock, curl and readlink are controlled fake CLIs. Success promotes the new release and cleans JSON. Failed acceptance correctly recreates the previous Compose release and leaves `current` unchanged, but fails `secret-json-cleaned`. This establishes shell control flow only; it does not establish real AWS, Docker or IAM behavior.

## Other reviewed controls

- Deployment workflow is main-only, depends on source/runtime/Sonar verification, requests protected `dev` environment and OIDC, publishes linux/amd64 SHA images, resolves digests, rejects High/Critical published-image findings, and invokes SSM deployment. GitHub environment/branch protections remain account-side prerequisites.
- OIDC trust binds the exact repository environment and audience. Deploy IAM limits image operations to the two repositories, release writes to `releases/*`, and Run Command to the instance plus AWS shell document. Required authorization-token and invocation-read wildcard permissions are visible.
- Host IAM can read the one runtime secret, pull the two repositories, read release-prefix objects and use managed SSM. IMDSv2 is required, metadata hop limit is one, disk is encrypted, and ingress rules are empty.
- Runtime secret values are populated outside Terraform; only the secret container/ARN enter state. State examples use encrypted S3 and native lock files. Bootstrap state/release buckets use public-access blocking, encryption, versioning and TLS policies; bootstrap state bucket is protected from destroy.
- Compose uses four database logins, Docker-private broker/database ports and loopback frontend access through SSM. Immutable app image digests are validated before rollout. `.env` validation constrains secrets to safe hex and the fake-CLI check confirms mode0600.
- Rollback is image restoration, not database reversal. Persistent volumes survive Compose recreation; instance replacement loses root-disk data. These dev limitations and migration compatibility requirements are documented.

## Remaining evidence boundary

No AWS credentials, provisioning, ECR publication, real OIDC assumption, SSM host execution, account-specific plan, actual cloud rollback or cloud business journey was performed. Those cannot be called verified from Terraform mock assertions or fake CLIs. Current Terraform validation/mock evidence must be read alongside this report before a prepared-scope WIN.

## Additional bootstrap blocker found during final review

`infra/aws-dev/user-data.sh` originally requests package `awscli2`, but AL2023 publishes `awscli-2`. Under `set -e`, a missing package aborts initialization before service enablement and Compose wrapper creation. The [official AWS AL2023 advisory](https://alas.aws.amazon.com/AL2023/ALAS2023-2026-3133.html) names `awscli-2` and its DNF command; [AL2023 documentation](https://docs.aws.amazon.com/linux/al2023/ug/awscli2.html) confirms the standard AMI already contains CLIv2. The root corrected the source to `awscli-2`. `al2023-package-probe.json` records an actual official linux/amd64 Amazon Linux container repository query resolving `awscli-2.noarch 2.36.47-4.amzn2023.0.1`; the minimal container has no CLI installed, so the trailing `rpm -q` exits2. This confirms package availability, not EC2 host startup. No scratch container remains.

## Final prepared-scope decision

No remaining release blocker was found in the reviewed prepared scope after the package-name and absolute secret-cleanup repairs. `terraform.txt` records valid dev/bootstrap configurations and one passing mocked security plan. AWS Compose resolves with explicitly synthetic environment values. Remote success and business-failure rollback orchestration pass2/2 with fake CLIs. The reference cloud environment was preparation rather than deployed evidence; this review applies the same honest boundary. Actual account IAM, SSM/user-data, cloud availability, restore safety and business acceptance remain unexecuted and must be verified after approved provisioning.
