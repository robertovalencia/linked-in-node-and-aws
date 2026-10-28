---
title: "WAF, DDoS protection and security findings"
topic: "WAF, DDoS protection and security findings"
last_researched: 2026-10-27
source_labels: Professional core curriculum; Official documentation; Explicit illustrative examples
---

# 64 · WAF, DDoS protection and security findings

**Prerequisites:** Ingress/security groups, ALB/TLS, IAM and encryption lessons 46–51 and 63.

[Previous lesson](63-kms-secrets-and-rotation.md) · [Next lesson](65-cloudwatch-agent-logs-metrics-and-alarms.md) · [Full syllabus](44-cloud-complete-syllabus-and-mastery-map.md)

## 1. Place each control at the right layer

A security group controls network reachability for associated resources. A web application firewall inspects supported HTTP request properties and applies rules at an associated resource. Neither replaces signed identity, input validation or resource ownership inside Node. An ALB accepting HTTPS does not make all backend requests authorized. Start by identifying which request crosses which trust boundary, then choose a control that can actually observe it.

AWS WAF works with supported application entry points, including ALB and CloudFront. A web ACL groups rules and default behavior. Rules can inspect properties such as URI, method, headers, body portions or client addresses. Inspection limits and supported integrations matter; do not describe a web ACL as arbitrary full-packet protection for PostgreSQL or Kafka. Those protocols need appropriate networking, authentication and encryption controls.

## 2. Understand rule behavior before blocking users

Allow/block/count actions have different consequences. A count-first evaluation can help measure how a candidate managed or custom rule matches legitimate traffic before a later reviewed blocking change. Scope a rate-based rule to the intended aggregation key and application segment. A rate-based rule is not a precise per-user business quota or a global guarantee that every request beyond one fixed number is blocked immediately.

Managed rule groups carry provider-maintained logic, but the application still owns compatibility and response handling. False positives need evidence and narrow rule tuning, not broad removal of the protective boundary. Consider forwarded addresses and trusted proxy configuration: blindly trusting a client-provided forwarding header can undermine an address-based control.

## 3. Distinguish prevention, detection and vulnerability inventory

Shield addresses DDoS protection; Standard and Advanced have different scope and commercial arrangements. WAF addresses supported application requests. GuardDuty produces threat findings from analyzed signals. Inspector identifies supported workload vulnerabilities/exposure. Security Hub collects/correlates security information, while posture-management controls answer configuration/compliance questions. A finding is evidence requiring investigation, not proof of a successful attack or automatic permission to delete a resource.

The repository’s npm audit and image scan are concrete software-maintenance checks. The parser/Multer repair shows why an audit can become red after an advisory is published even when application source has not changed. Passing that audit does not establish WAF coverage or malicious-activity detection.

## 4. Build an evidence-driven response

For a finding, record resource identity, affected version or condition, time, account/region, relevant request or activity evidence, and an owner. Protect logs that contain addresses or request metadata. Separate an available attack path from exploitation evidence. Never include bearer tokens, secret values or whole credential files in an incident note.

## 5. Keep security additions proportionate

An isolated interview environment does not automatically need every paid security feature. The deployment owner must compare coverage, integration requirements, data volume, retention and costs before proposing changes. This lesson does not enable a service, create a web ACL or estimate a subscription.

## Example and current-project boundary

**New design exercise; not implemented:** diagram client → WAF-associated ALB → application SG → database SG. Mark the TLS termination point and the application’s JWT/ownership checks. On a second diagram show the current no-ingress SSM path. Adding public ingress creates a new exposure decision; a named security product alone does not justify it.

Read [the real dependency maintenance example](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/docs/dependency-security.md) to distinguish demonstrated package remediation from these new service concepts.

## Practice with observable evidence

1. Build a threat/control table for SQL injection attempts, unauthenticated API use, public database reachability, leaked credentials and vulnerable dependencies.
2. For each row name what can prevent it, what could detect it, which evidence you would inspect and one remaining limitation.
3. Create a synthetic request classification table containing legitimate search/login traffic and suspicious inputs. Predict count versus block outcomes without contacting an AWS endpoint.
4. Write an investigation note for a hypothetical vulnerability finding, clearly separating affected software from proof of exploitation.

**Expected evidence:** two boundary diagrams and a control matrix that never credits WAF with database authentication or application ownership enforcement.

## Recall and interview defense

### Does adding ingress make the project more secure?

No. Ingress grants a path. A realistic ALB design may require narrowly scoped rules, but the safety argument is that only required paths are allowed and all other controls remain effective.

### Does an Inspector or GuardDuty finding mean the application was compromised?

Not automatically. State what the finding establishes, correlate evidence, and investigate before asserting an incident.

### What does a passing npm audit prove?

It reports no matching advisories for the audited dependency graph at that moment. It does not establish complete security.

## Mastery gate

Explain the mechanism without reading, show the stated evidence, identify a failure case and say which facts were tested locally versus merely proposed for AWS. Keep personal notes in your existing protected progress area. Learning a service does not require deploying it in the portfolio.

## References

Official sources checked on 2026-10-27. These teach mechanisms; any account-specific cost comparison, service selection or provisioning belongs to the deployment chat and requires its own current evidence.

- [AWS WAF concepts](https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html)
- [AWS Shield](https://docs.aws.amazon.com/waf/latest/developerguide/shield-chapter.html)
- [GuardDuty purpose](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html)
- [Inspector purpose](https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html)
