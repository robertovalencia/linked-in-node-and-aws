---
title: "AWS accounts, governance, and landing zones"
topic: "AWS accounts, governance, and landing zones"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 45 · AWS accounts, governance, and landing zones

**Prerequisites:** 44; distinguish AWS account, Region, identity, and workload.

[Previous: 44](44-cloud-complete-syllabus-and-mastery-map.md) · [Next: 46](46-iam-policy-evaluation-and-federation.md) · [Study path](../README.md)

**Implementation boundary:** AWS Organizations, Control Tower, organization policies, and a multi-account landing zone are proposed learning topics, not resources declared by this project.

A landing zone is the governed foundation into which teams deploy workloads: accounts, workforce access, logging, network conventions, and baseline controls. AWS Organizations manages a collection of accounts. An organizational unit (OU) groups accounts for policy administration; it is not a network segment. AWS Control Tower coordinates a prescriptive landing zone using other AWS services. Begin with the organization’s responsibilities and isolation needs, rather than drawing an account for every application container.

## 1. Define account boundaries using failure and trust

Separate production from experimentation when their access, change cadence, or failure tolerance differ. Consider dedicated security and log archive accounts so a compromised workload role cannot freely rewrite its own evidence. Write who owns each account, how incidents escalate, and where recovery access lives. An account boundary gives useful isolation, but cross-account trust and resource policies can deliberately reconnect accounts. Draw those connections so the isolation claim can be examined.

## 2. Understand policy inheritance before designing OUs

A service control policy (SCP) limits the permissions available to governed member-account principals; it does not grant permission. Effective access still needs applicable IAM grants and is affected by explicit denies. OUs let administrators apply policy to groups, and inherited restrictions matter along the path to an account. Do not describe an SCP as a firewall or assume the same policy behavior applies to the organization management account. Review exceptions against the documented scope.

## 3. Separate workforce identity from application identity

Use IAM Identity Center concepts for human access across accounts, with an external identity provider where appropriate. A permission set describes access that is provisioned into assigned accounts. Application workloads instead use service roles and temporary credentials. Keep emergency access independent enough to handle an identity-provider outage, and protect and monitor it. A team spreadsheet listing administrators is not an enforcement mechanism; the assignments, trust policies, and session behavior must agree.

## 4. Establish controls and evidence ownership

A preventive control blocks an unwanted action; a detective control reports a condition after observation. Control Tower supplies governance mechanisms, but the organization still decides ownership, exception handling, and remediation. Specify centralized audit collection, retention, access separation, and how a new account enters the baseline. Record supported Regions and required services from current documentation rather than assuming a landing zone configures every account or Region automatically.

## 5. Connect governance to infrastructure delivery

Terraform roots should target explicit accounts and Regions through intended provider configurations and roles. Review the account identifier and permitted role before evaluating individual resource changes. A module cannot substitute for organization-level governance: application teams should not need broad organization administration to launch a service. Design a workflow where baseline owners and workload owners have clear change boundaries, and where policy rejection is an understandable signal rather than a reason to use administrator credentials.

## Source or illustrative example

**New illustrative example, not implemented:** an OU named `Sandbox` contains disposable learning accounts; `Workloads` contains separate development and production accounts; a security team owns audit access. A “deny unsupported Regions” policy is only a proposed control. Before using one, analyze global services, existing dependencies, and emergency exceptions. The example is an organizational design sketch, not a deployable policy or a claim about the user’s AWS organization.

## Safe exercise

Create a local account-governance worksheet without contacting AWS:

```sh
python3 - <<'PY'
accounts = [('security', 'security-team'), ('dev', 'app-team'), ('prod', 'app-team')]
assert len({name for name, _ in accounts}) == len(accounts)
for name, owner in accounts:
    print(f'{name}: owner={owner}; access-review=required')
PY
```

Expected outcome: three unique logical accounts and an explicit owner for each. Extend the worksheet with audit destination, allowed deployment role, and emergency-access owner. Explain which entries are requirements and which need later implementation evidence.

## Failure diagnosis

An AccessDenied after moving an account into an OU may result from inherited organization policy, not a missing application-role grant. Check the complete policy path and principal scope before editing IAM. Missing audit records can mean an ungoverned Region, a broken delivery permission, or an incorrect assumption about service coverage. A successful account creation says nothing about baseline enrollment. Investigate identity-provider availability separately from workload health when humans cannot sign in but applications continue operating.

## Recall and answers

### Does an SCP let a developer create an EC2 instance?

No. It can limit available permissions; a suitable IAM allow is still required.

### Why separate log ownership?

To reduce the ability of a compromised workload identity to alter the evidence needed to investigate that compromise.

## Mastery check

Draw a proposed organization with ownership and cross-account trust arrows. Explain an inherited-deny incident and a workforce sign-in outage. A passing explanation distinguishes account governance, identity permissions, network boundaries, and application authorization without claiming this project has deployed a landing zone.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [AWS Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html)
- [AWS Control Tower](https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html)
- [IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)
- [SCP scope and behavior](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)
