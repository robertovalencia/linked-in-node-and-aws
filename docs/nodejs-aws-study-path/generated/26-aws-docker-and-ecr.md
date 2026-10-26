---
title: "Docker images, ECR, tags, digests and scanning"
topic: "Docker images, ECR, tags, digests and scanning"
last_researched: 2026-10-26
source_commit: 9bb88515f14067feb23611c6851c03ca8fbc89b6
---

# 26 · Docker images, ECR, tags, digests and scanning

**Prerequisites:** 14 plus25; image versus container and CPU architecture.

[Previous: 25](25-aws-ec2-ebs-and-bootstrap.md) · [Next: 27](27-aws-s3-artifacts-and-secrets.md) · [AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md)

## 1. Separate build artifact from running instance

A Dockerfile builds an image; an image is stored in a registry; a container runs that image with configuration. The two application repositories are backend and frontend. Four Node capabilities reuse the backend image with different `SERVICE`, port and database configuration. One image does not mean one runtime service.

## 2. Give release identity a chain

A source commit identifies repository content. An image tag labels an image. A digest identifies registry image content. The release script associates an exact source SHA with images, resolves ECR digests, and places digest references in the manifest. Terraform makes app tags immutable. A digest still needs source/build provenance; it does not by itself prove who built the image or which commit it represents.

## 3. Understand pull and push permissions

The release producer uploads images. The host pulls them. Their policies differ. Registry login obtains authorization but does not bypass repository permissions. The script targets linux/amd64 to match the host. Local image availability on a developer laptop does not establish registry publication or host pull success.

## 4. Treat scanning as an enforced check with limits

ECR scan-on-push is configured. The release path additionally scans the actual digest images using the pinned Trivy version and rejects High/Critical findings, including unfixed ones. Vulnerability results can change as databases update. A scan says nothing about provider ownership rules or a leaked application key unless those are separately tested/detected.

## 5. Keep lifecycle and rollback compatible

The ECR lifecycle rule expires untagged images after seven days. Immutable tagged releases remain until deliberate cleanup or repository destruction. A rollback needs the old digest to remain available. `force_delete=true` is a final dev teardown setting, not automatic expiry and not a production retention recommendation.

## Walk the real project

[infra/aws-dev/main.tf · lines 46–54](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L46-L54)

```hcl
resource "aws_ecr_repository" "app" {
  for_each             = toset(["backend", "frontend"])
  name                 = "${local.name}/${each.key}"
  image_tag_mutability = "IMMUTABLE"
  force_delete         = true
  image_scanning_configuration { scan_on_push = true }
  encryption_configuration { encryption_type = "AES256" }
}
resource "aws_ecr_lifecycle_policy" "app" {
```

[.github/workflows/deploy-dev.yml · lines 81–89](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/.github/workflows/deploy-dev.yml#L81-L89)

```yaml
            digest=$(aws ecr batch-get-image --repository-name "${repo#*/}" --image-ids "imageTag=$GITHUB_SHA" --query 'images[0].imageId.imageDigest' --output text)
            if [[ ! "$digest" =~ ^sha256:[a-f0-9]{64}$ ]]; then
              docker buildx build --platform linux/amd64 --label "org.opencontainers.image.revision=$GITHUB_SHA" --push --tag "$repo:$GITHUB_SHA" "$app"
              digest=$(aws ecr batch-get-image --repository-name "${repo#*/}" --image-ids "imageTag=$GITHUB_SHA" --query 'images[0].imageId.imageDigest' --output text)
            fi
            [[ "$digest" =~ ^sha256:[a-f0-9]{64}$ ]]
            echo "${app^^}_IMAGE=$repo@$digest" >> "$GITHUB_ENV"
          done
      - name: Scan the actual published images
```

Follow a digest from `batch-get-image` to `BACKEND_IMAGE`/`FRONTEND_IMAGE`, then to the manifest and Compose. Find the exact point where source-SHA verification is checked before publication in the selected local helper. The optional workflow is another path, not proof it executed.

## Practice step by step

1. Write sourceSHA → tag → digest → manifest → container as five distinct identities.
2. Read the backend Dockerfile and frontend Dockerfile; list which directory each build consumes.
3. Read-only local exercise: use `docker image inspect` for an already-built project image; compare image ID and repository digest fields without assuming they are identical concepts.
4. Predict a retry under an existing immutable tag and explain why the helper reuses and rescans it.

**Expected evidence:** A release-identity diagram and an explanation of build architecture, pull/push permissions and retained rollback artifacts.

## Check your understanding

### Can I use `latest` to prove which source was deployed?

A mutable label is insufficient. This project carries source identity plus resolved digest references and verification evidence.

### Does an immutable tag guarantee a vulnerability-free application?

No. Immutability stabilizes naming; scanning and behavior/security review address different risks.

Do not mark this lesson complete until you can show the evidence and explain the result without reading the answer. Record your attempt and remaining question in your personal study notes; generated lessons are not personal progress records.

## References

Code excerpts are pinned to the inspected project revision `9bb8851`. They describe source, not proof that AWS resources were deployed. Official documentation was checked on 2026-10-26; verify account policies and selected tool versions before a real deployment.

- [ECR tag immutability](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-tag-mutability.html)
- [ECR image scanning](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html)
