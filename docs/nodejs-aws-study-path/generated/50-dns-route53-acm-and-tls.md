---
title: "DNS, Route 53, ACM, and TLS"
topic: "DNS, Route 53, ACM, and TLS"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 50 · DNS, Route 53, ACM, and TLS

**Prerequisites:** 47–49; basic HTTP hostnames and certificates.

[Previous: 49](49-private-connectivity-nat-and-endpoints.md) · [Next: 51](51-alb-target-groups-and-health-checks.md) · [Study path](../README.md)

**Pinned baseline boundary:** At the source revision linked below, Route53 hosted zones, ACM certificates and a public TLS entry point were not declared in the EC2 development root; its browser access used an authenticated SSM tunnel. Later verified certificate-only evidence appears at the end of this lesson. Application HTTPS remains pending.

DNS maps names to records that help clients find services. A hosted zone is an authoritative collection of records for a domain. TLS protects transport and lets a client validate the server name against a certificate and trusted issuer. AWS Certificate Manager (ACM) manages certificates for supported integrations; Route 53 manages DNS functions. A successful DNS answer does not establish a healthy application, and an issued certificate does not automatically attach itself to a listener.

## 1. Trace resolution from delegation to answer

A registrar delegates a domain to authoritative name servers, and those servers answer records in the hosted zone. A public hosted zone serves public DNS; a private hosted zone answers within associated VPC contexts. An A record concerns IPv4 and an AAAA record IPv6. Route 53 alias records can target supported AWS resources. Explain the difference between creating a hosted zone and updating the domain’s actual delegation; either can exist without the other working.

## 2. Choose the public service identity

A browser requesting `app.example.com` sends a hostname and expects a certificate valid for it. The endpoint might be CloudFront or a regional ALB, but that is an architecture decision. Wildcard coverage has specific name-matching rules and should not be assumed to include every depth or the zone apex. Define the names, redirect behavior, and API origin before requesting a certificate, so the DNS and TLS design matches the application’s actual URLs.

## 3. Understand validation and certificate location

ACM DNS validation proves control of requested names through validation records. Preserve the required records for managed renewal rather than deleting them after issuance. For the conventional CloudFront integration, request or import the ACM viewer certificate in US East (N. Virginia), `us-east-1`; a regional ALB uses a certificate in its own Region. Check the integration documentation before provisioning. A certificate present in the wrong Region may not be available for the intended listener.

## 4. Review every TLS hop

Viewer-to-edge TLS and edge-to-origin TLS are separate connections. Terminating HTTPS at a load balancer does not automatically encrypt traffic to a backend target. Define origin protocol, certificate validation, and trust requirements explicitly. Application cookies, forwarded headers, secure redirects, and absolute URLs must reflect the client-facing scheme. Avoid disabling certificate verification to hide a hostname mismatch; repair the hostname, certificate chain, or routing configuration that caused it.

## 5. Plan change propagation and renewal evidence

DNS caching depends on time to live and resolver behavior, so changes may not be observed instantly everywhere. A lower TTL can help a planned transition but cannot revoke already cached answers immediately. Record ownership of delegation, validation records, listener association, expiry monitoring, and incident response. Terraform references can express certificate-to-listener dependencies, but source validation cannot prove public DNS delegation or successful managed renewal. These require later authorized operational checks.

## Source or illustrative example

**New illustrative example, not deployed:** `app.example.com` is an alias to a future ALB; a regional ACM certificate covers that name; the ALB forwards to private application targets. A separate static-site CloudFront design would need its own viewer-certificate Region decision. `example.com` is a documentation domain and none of these records should be created as part of this course.

## Safe exercise

Inspect a public documentation domain without AWS account access:

```sh
dig example.com A +short
dig example.com AAAA +short
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates
```

Expected outcome: DNS answers and certificate identity/validity metadata when public network tools are available. Exact addresses and dates may vary. If network access is unavailable, sketch the same resolution and TLS sequence using redacted sample fields. This does not inspect or validate the project’s AWS environment.

## Failure diagnosis

If the name does not resolve, investigate delegation, authoritative records, and resolver scope before changing TLS. If DNS resolves but the browser reports a name mismatch, compare the requested hostname and certificate subject alternative names. If TLS succeeds but requests return 502, investigate the origin hop and backend health. Renewal trouble may involve deleted validation records or unsupported certificate handling; confirm certificate type and integration rather than assuming every imported certificate renews automatically.

## Recall and answers

### Can a valid certificate fix a missing DNS delegation?

No. Name resolution and certificate validation are separate stages.

### Why does the certificate Region matter?

Integrated services look for certificates in their supported location; conventional CloudFront viewer certificates use us-east-1, while regional ALBs use their own Region.

## Mastery check

Draw browser → DNS → public endpoint → private origin and label every hostname, certificate, and TLS termination. Diagnose a missing DNS record, a wrong-name certificate, and an origin TLS error. Explicitly identify which checks are local/public demonstrations and which require future project deployment evidence.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [Route 53 overview](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html)
- [ACM overview](https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html)
- [CloudFront origins](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistS3AndCustomOrigins.html)
- [CloudFront certificate requirements](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cnames-and-https-requirements.html)


## Later project evidence: certificate gate only

The original source anchors above describe the EC2/SSM baseline. On 2026-10-28 the deployment owner reported the later certificate as ISSUED and unused. Study the [sanitized issuance evidence](https://github.com/robertovalencia/linked-in-node-and-aws/blob/319392bea09e75f78edd196bcb8eed3ffc1f5b95/docs/evidence/certificate-request/issuance.json) and [DNS/certificate guide](https://github.com/robertovalencia/linked-in-node-and-aws/blob/319392bea09e75f78edd196bcb8eed3ffc1f5b95/docs/aws-free-test-hostname.md). An unused issued certificate proves neither application HTTPS nor renewal readiness. ALB, application and operational gates remain pending; see the [owner coordination record](../deployment-coordination.json).


## Recognize the console screen

Use the [AWS visual study guide](../visuals/README.md) to identify the console fields and connect them to source. Official AWS examples demonstrate concepts and are not screenshots of this project’s deployment.
