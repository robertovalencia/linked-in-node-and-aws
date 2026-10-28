---
title: "CloudFront, private S3 origins, and cache correctness"
topic: "CloudFront, private S3 origins, and cache correctness"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 52 · CloudFront, private S3 origins, and cache correctness

**Prerequisites:** 50–51; HTTP headers and browser assets.

[Previous: 51](51-alb-target-groups-and-health-checks.md) · [Next: 53](53-ecs-fargate-tasks-and-services.md) · [Study path](../README.md)

**Implementation boundary:** The project S3 release bucket stores deployment artifacts. It is not a CloudFront website origin. CloudFront and origin access control below are proposed learning designs.

CloudFront is a content delivery network that serves requests through edge locations and retrieves content from configured origins when needed. A cache key identifies which requests may share a stored response. A cache policy selects key inputs and freshness behavior; an origin request policy controls additional values forwarded to the origin. A private S3 origin with origin access control (OAC) differs from an S3 static website endpoint, which has different access and protocol characteristics.

## 1. Separate static delivery from deployment artifacts

Choose a distinct content boundary for public web assets rather than reusing a release bucket merely because both use S3. Fingerprinted JavaScript and CSS can use long-lived caching because a content change changes the filename. The HTML entry document generally needs a shorter freshness policy so clients discover new asset references. Preserve old asset versions long enough for clients loading an earlier HTML document. A release manifest and a viewer-facing asset have different consumers and permissions.

## 2. Protect the origin without confusing viewer access

For a conventional private S3 REST origin, configure OAC and a bucket policy that permits the intended distribution, while retaining appropriate S3 public-access controls. A website endpoint is handled as a custom origin and cannot be treated as the same private REST-origin pattern. Origin restrictions prevent direct unauthorized origin reads; they do not automatically authenticate CloudFront viewers. Signed URLs, cookies, or application authorization are separate choices for private content.

## 3. Design cache keys around response variation

List every input that changes a response: path, selected query parameters, headers, cookies, locale, tenant, or authenticated user. If two users can receive different content for one key, shared caching can disclose data. Unnecessary key inputs also reduce cache reuse. An origin request policy can forward a value without automatically including it in the key, so a forwarded authorization-related value deserves special scrutiny. Prefer explicit non-caching behavior for sensitive personalized API routes unless a safe design is established.

## 4. Control freshness, errors, and invalidation

TTL controls how long cached content is considered fresh, subject to policy and response headers. A positive minimum TTL can cause content to be cached despite origin directives that might otherwise prevent caching; review the actual policy. Error caching can preserve a temporary 403 or 404 after its underlying cause is fixed. Invalidation requests expire selected cached paths, but versioned filenames often make release reasoning clearer. Do not confuse browser caches with CloudFront’s independent edge caches.

## 5. Connect edge delivery to TLS and observability

Verify the viewer hostname and certificate arrangement from lesson 50, then separately define HTTPS to the origin where supported. Record response status, cache hit or miss, origin status, and request identity without leaking tokens in logs. A successful distribution update is not proof that every edge and browser immediately serves the intended revision. Validate representative assets, HTML, and API behaviors after a future authorized release, with explicit expectations for propagation and retained old content.

## Source or illustrative example

**New illustrative cache design:** `/assets/app.abcd1234.js` is immutable public content; `/index.html` is refreshed frequently; `/api/me` is a personalized route with caching disabled. This is not current CloudFront configuration. **Actual source anchor:** [S3 release bucket controls](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/main.tf) describe artifact storage and should not be relabeled as a static-site distribution.

## Safe exercise

Run this local key-collision demonstration:

```sh
node --input-type=module <<'JS'
const key = r => r.path;
const a = {path:'/api/me', user:'alice'};
const b = {path:'/api/me', user:'bob'};
console.log(key(a) === key(b));
console.log(a.user !== b.user);
JS
```

Expected outcome: `true`, `true`: two different user contexts collide under a path-only key. Write why merely forwarding a user header to an origin does not fix a shared-cache key. Then propose a safe public-asset policy and a non-caching personalized route without constructing AWS resources.

## Failure diagnosis

If a new deployment serves old HTML, inspect browser and edge freshness independently, then the origin object version. A private-origin 403 may involve OAC, bucket policy, wrong object key, or encryption access rather than viewer authentication. If one user sees another user’s content, disable the unsafe caching path through the authorized incident process and inspect key variation. Do not use a blanket SPA error rewrite to conceal missing JavaScript assets; wrong content types can create misleading browser failures.

## Recall and answers

### Does an origin request policy automatically vary the cache key?

No. Forwarded inputs and cache-key inputs are distinct policy decisions.

### Can a private S3 origin still serve public CloudFront viewers?

Yes. Origin access restrictions and viewer authorization solve different access problems.

## Mastery check

Define policies for immutable assets, entry HTML, personalized API responses, and cached errors. Explain a cross-user cache collision and a private-origin 403. Point to the existing artifact bucket only for its actual purpose, and label the website architecture as proposed.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [CloudFront origins](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistS3AndCustomOrigins.html)
- [CloudFront cache key policies](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/controlling-the-cache-key.html)
- [Amazon S3 overview](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- [S3 origin access control](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)
- [CloudFront TTL and key settings](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cache-key-understand-cache-policy.html)
