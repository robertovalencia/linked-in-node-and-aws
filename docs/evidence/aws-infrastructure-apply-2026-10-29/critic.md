# Independent critic — actual infrastructure apply, 29 October 2026

**FAIL: the approved infrastructure did not finish. Paid partial allocations remain.** The exact approved binary was executed once; Terraform exited 1. There were 99 successful create events, while actual persisted state contains 100 managed instances because the partially configured ALB is saved as tainted. Eleven approved instances are absent. This is not an operational marketplace or a successful infrastructure deployment.

## Execution and authorization

I independently read `AGENTS.md`, the final approval package, the private one-shot runner and the actual post-run evidence. The binary SHA256 remains `2fd776a529ab587759500bf71e43c5f461a528034db2942d5af2f664fe222b56`. Runner guards bind the reviewed source/provider lock, real S3 backend/default workspace, account 772641336063, Ohio, current cost/preflight receipts and the 111-create artifact. There was no alternate plan, activation, operator bootstrap, repair apply, account upgrade, cleanup apply, controller or reminder. The critic used read-only CLI requests through the helper's cleaned environment and did not read secret values.

The initial sandboxed collection could not resolve AWS endpoints. It is preserved under `network-unavailable-attempt/` and establishes no infrastructure controls. The subsequent network-enabled collection independently reached the intended account. Its private raw evidence and corrected consolidated summary are under `private/`. Raw plans, state and exact client ingress address remain private.

## Blocking actual results

1. **RDS is absent.** The approved seven-day backup retention was rejected with `FreeTierRestrictionError`. A later scoped `describe-db-instances` returned `DBInstanceNotFound`. The parameter group exists with `rds.force_ssl=1` and `log_min_error_statement=panic`, but there is no database to demonstrate runtime TLS, encryption, deletion protection, backup or recovery. Neither upgrading the account nor weakening approved retention/protections is authorized by this apply approval.
2. **ALB exists, but HTTPS was never installed.** The actual ALB is active and Terraform marks it tainted. AWS rejected its access-log attribute update because the operations bucket permission was not accepted. Live reads show zero listeners, `access_logs.s3.enabled=false` and `routing.http.drop_invalid_header_fields.enabled=false`. There is no live HTTPS certificate binding, approved-host forwarding rule or default 403 behavior to verify. The target group exists and has no targets.
3. **Broker private DNS is absent.** The direct Route53 write was rejected because the private hosted zone can only be managed through AWS Cloud Map. Live private-zone records contain no broker A record. Five Cloud Map service definitions exist with zero registered instances.
4. **All seven planned alarms are absent.** They must not be reported as working or delivering notifications. No notification destination was part of the approval.

The eleven absent state addresses are RDS, the HTTPS listener and host rule, the broker DNS record and seven alarms. The ALB is an additional incomplete allocation rather than an absent address. A generic Terraform output containing the intended application URL is not evidence that the URL works.

## Verified remaining controls

- Live SG rules exactly match all 35 approved state rule IDs and trust paths, with no extra rules in the nine managed groups. ALB ingress is one approved IPv4 /32 on TCP443 only. Database and broker ingress use the exact intended SG references; bootstrap has no inbound rule. An independent outside-source denial probe was not performed.
- The broker EC2 instance is running privately, has no public IPv4, and its EC2 instance/system checks pass. IMDSv2 is required with hop limit 1 and IPv6 metadata disabled. Its one 40GiB gp3 root volume is encrypted and deletes on instance termination. This proves allocation controls, not a running authenticated Kafka broker.
- Four subnets do not autoassign public IPs. Public subnets route through the Internet gateway; the active private subnet routes through the available public zonal NAT; standby has no Internet default route. One S3 gateway endpoint exists.
- The two ECR repositories are immutable, scan on push and use AES256 encryption. The operations bucket has all four public-access blocks, AES256 encryption, versioning, seven-day current/noncurrent lifecycle and a plaintext-transport deny. Its initial `force_destroy=false` remains in persisted state. These bucket controls did not make ALB log delivery succeed.
- Detailed live prefix reads confirm all eight log groups retain seven days. The earlier pattern-based response omitted retention fields by API design; it is superseded by the detailed reads, not a real retention failure.
- All six runtime secrets have metadata but no versions. No RDS-managed master secret appears in saved state or outputs; there is no created DB instance to bind one. An account-wide orphan-secret inventory was not performed. The approved host user-data enables a retrying broker bootstrap service; no successful execution, populated credentials, Kafka authentication or app bootstrap was demonstrated.
- Actual ECS service lists, RUNNING/PENDING task lists and project-family task-definition lists are empty; cluster aggregate counts are zero. No application was activated.
- The existing ACM certificate remains ISSUED for the intended hostname with export disabled. Independent current hashes still match the separate preapply certificate and bootstrap-state hashes. Those states and the certificate are preserved.

## Actual transport probes and clock

The current probe source matched the private approved /32. Two reserved `curl --connect-to` probes preserved the real hostname/SNI, normal route and certificate verification; one kept the approved HTTP Host and one used an unapproved Host. Both failed to connect with curl exit7/HTTP000, consistent with zero listeners. There was no TLS handshake, certificate validation result, 503 empty-target response or 403 host-denial response to claim. DNS was not changed.

The conservative first paid-resource create started at **2026-10-29 21:51:25.219221 UTC**, for a runtime secret; first successful paid completion followed at 21:51:25.584766 UTC. The operator deadline remains **30 October 21:51:25 UTC / 5:51:25 p.m. EDT**, including this failed apply. Recommended human return is **30 October 19:51:25 UTC / 3:51:25 p.m. EDT** for renewal and exact cleanup/teardown review. This is an operational deadline derived from a real Terraform create-start event, not a proven AWS billing-meter timestamp. The raw Terraform timestamps used an EDT offset; the preserved derived UTC clock correctly normalizes the same instants. No timer, reminder or unattended cleanup exists.

## Largest gap and required next boundary

The largest gap is treating partial resource allocation as completed infrastructure. The repair in this execution is truthful inventory, preserved errors/state, normalized timing and an activation stop; no cloud repair was applied. The three actual service rejections require a newly prepared, costed and reviewed repair or cleanup proposal. The paid resources continue to exist until approved operator action and actual deletion verification; failure did not roll them back or reset the 24-hour clock. A new saved plan may replace the tainted ALB and therefore must be reviewed from real state, not assumed to be the original 111-create artifact.

Private evidence: `private/final-evidence-summary.json`, raw per-command JSON, `private/followup-summary.json`, `private/tls-summary.json`; original apply/state/clock receipts remain in the repository's private run directory. This review makes no application acceptance, broker runtime, database recovery, image security, notification delivery or automatic cleanup claim.
