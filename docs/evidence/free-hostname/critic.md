# Independent critic: free test hostname for the planned ALB

Reviewed 2026-10-27. Scope: provider documentation and public DNS only. No AWS operations, DNS writes, signup, credentials, certificate request, source edits, or provisioning were performed by this critic.

## Verdict

Conditionally suitable for the existing 24-hour HTTPS ALB demonstration. A dynv6-owned free zone with a child `app` CNAME is a plausible route without domain registration fees or topology changes. This is a prepared option, not a reserved hostname or verified certificate integration. Do not apply paid infrastructure until the user controls the zone, exact ACM validation CNAME resolves publicly, ACM reports ISSUED in us-east-2, allowed client CIDRs are reviewed, and the fresh final plan/cost is approved.

Biggest remaining gap: there is no registered, user-controlled test zone and no actual ACM issuance evidence. NXDOMAIN is not a registration availability check.

## Independent public DNS observations

At 2026-10-27 17:48 EDT (21:48 UTC):

- `dig @1.1.1.1 linked-in-node-rv.dynv6.net A` returned NXDOMAIN, zero answers.
- `dig @ns1.dynv6.com linked-in-node-rv.dynv6.net A +norecurse` returned authoritative (`aa`) NXDOMAIN, zero answers.
- `dig @1.1.1.1 dynv6.net CAA` returned NOERROR, zero answers. This is a point-in-time parent observation, not proof of future effective CAA at the new zone or app name.
- `dynv6.net NS` returned ns1.dynv6.com, ns2.dynv6.com, ns3.dynv6.com.

Initial sandbox calls could not bind DNS sockets. Read-only escalated calls above succeeded. No DNS entries were created.

## Primary-source support

- [dynv6 homepage](https://dynv6.com/): free public hostnames and DNS service; no enterprise SLA or DDoS protection. Suitable only for this noncritical temporary demonstration.
- [dynv6 official REST specification](https://dynv6.github.io/api-spec/): owned zones support CNAME and CAA records; zone registration and record operations require authenticated account ownership. It does not completely specify nested-relative name or trailing-dot parsing behavior.
- [dynv6 official changelog](https://dynv6.com/docs/changelog): underscore DNS records supported since 2015; CAA supported since 2019/20. This supports the expected ACM underscore record capability, but does not substitute for an actual record creation/readback test.
- [dynv6 Terms, updated 2026-10-21](https://dynv6.com/terms): service is free and may be changed or discontinued; inactive accounts may be deleted, particularly when IPs do not change regularly; disposable email is prohibited; excessive API traffic may be throttled. There is no promised perpetual ownership or numeric quota documented on these reviewed pages. Do not add unnecessary polling or imply a durable production domain.
- [AWS ACM DNS validation](https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html): user must control public DNS, place the exact validation CNAME, avoid duplicated zone suffixes, and preserve it for automatic renewal. More than five chained CNAMEs fail validation. ACM times out after 72 hours without validation.
- [AWS ACM DNS troubleshooting](https://docs.aws.amazon.com/acm/latest/userguide/troubleshooting-DNS-validation.html): validation CNAME owner must retain its leading underscore; provider handling of trailing periods differs; CAA can block issuance even when validation DNS appears correct.

## Conditions for the concrete guide

1. Reserve `linked-in-node-rv.dynv6.net` only if the provider offers it; otherwise select another available free zone and adapt every hostname. Never claim it is already available/reserved from NXDOMAIN.
2. Use `app.<owned-zone>` for the application, not a CNAME at the owned zone apex. A/AAAA records must not coexist at the same `app` owner name as its CNAME.
3. For ACM hostname `app.<owned-zone>`, intended validation owner is `_ACTUAL_TOKEN.app.<owned-zone>.`, with the exact ACM-provided `_ACTUAL_VALUE.acm-validations.aws.` target. An example token is not a real record. In a relative-name UI the owner would be `_ACTUAL_TOKEN.app`; verify the provider-generated fully qualified result. The official API schema does not prove this UI format.
4. Preserve an absolute external target. If the UI changes the trailing period, inspect `dig CNAME` for the exact resulting target and reject accidental zone-suffix appending. Do not strip the leading owner underscore or invent a replacement value.
5. After ALB provisioning is separately approved, point `app.<owned-zone>` to the actual Terraform ALB DNS output using CNAME. Do not pin changing ALB A/AAAA addresses or run a dynamic-IP update client for this path.
6. Before issuance recheck public resolution and effective CAA; then use ACM ISSUED as the activation gate. No certificate issuance guarantee can be made from provider documentation alone.
7. TLS certificate and free DNS do not remove AWS ALB/NAT/ECS/RDS charges. Existing $8.32/24h active estimate remains the current estimate until a new saved plan or assumptions change it. No HTTP fallback, topology expansion, broad client ingress, domain purchase, or paid resource activation is justified by this hostname choice.
8. Teardown removes the application CNAME before releasing ownership, removes obsolete validation records when certificate cleanup is complete, and destroys separately approved AWS resources. A leftover DNS CNAME to a deleted/reassigned endpoint is not a complete teardown.

## Final documentation review

**PASS for preparation/documentation scope.** Read the completed `docs/aws-free-test-hostname.md` after initial research. It accurately preserves the conditional nature of the provider choice, unavailable ownership/issuance evidence, existing topology/costs and separate provisioning approval. It covers the eight conditions above, exact-name DNS verification, child CNAME conflicts, actual ACM ISSUED activation, narrow ingress and teardown. The linked Terms URL `https://dynv6.com/terms` was independently opened successfully and shows last updated 2026-10-21. The AWS CAA troubleshooting link opens successfully. The documented `/health` path exists in nginx and acceptance CLI positional arguments match the real script.

No meaningful source/runtime test is justified for this documentation-only change. No infrastructure or application behavior was changed or tested in AWS. Biggest remaining gap remains user-controlled zone and real ACM validation/issuance, followed by the independently approved deployment and ALB/user-journey tests.
