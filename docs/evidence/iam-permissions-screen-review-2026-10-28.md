# Independent IAM screenshot follow-up review

**Verdict: PASS for documentation preparation.** Reviewed 2026-10-28. This review does not approve or execute IAM user creation, credential entry, MFA assignment, policy attachment, permission-boundary changes, invitations or AWS provisioning.

## Scope and actual checks

Applied the `aws-iam` skill's instruction to verify IAM claims against current official documentation. Independently inspected the actual original user-supplied PNG, read the staged `03-iam-user-permissions.md`, the identity clarification, guide navigation, and image provenance manifest. Independently retrieved current official `ViewOnlyAccess`, `AWSCertificateManagerReadOnly`, and permissions-boundary documentation.

## Visual/privacy verdict

The actual image shows IAM Create user, Step 2 Set permissions; Copy permissions selected; Users (0); Attach policies directly available; optional permissions boundary checked; and the boundary policy section. The account/Region, proposed username, Step 1 console access/password settings, and final creation result are not visible. The lower-right thumbnail is a duplicate capture preview in the supplied original, not unrelated private content.

No credential, username, entered email, account menu, exact private client CIDR or unrelated browser content is visible. The staged PNG is an exact byte copy of the original attachment. Both have SHA-256 `e7ab0e2d481fd411b35041aeb246af90a302767feaaaf4bc3f242057f88498ec`, matching the provenance manifest.

## Caption/policy verdict

The card matches the visible fields and correctly limits its evidence: wizard in progress, no completed user, no inferred account association, no proof of console-password support. The cross-reference clarifies why a CLI assumed-role name does not establish the browser account's sign-up model. It preserves the official conditional restriction on IAM console users in the new project-account experience.

The two policies are accurately described as a broad viewing baseline, not a resource-scoped production or Terraform operator policy. Current official ViewOnlyAccess v46 provides resource/basic-metadata viewing; current AWSCertificateManagerReadOnly v7 supplies certificate description and other ACM read operations. The card does not promise every panel or log content will be accessible, and it does not recommend AdministratorAccess to resolve access errors.

The boundary explanation correctly distinguishes access grants from the identity-policy ceiling. It warns that setting ViewOnlyAccess only as a boundary can constrain additional ACM reads. The optional-boundary advice is expressly confined to an uncreated basic study user; existing or administrator-required guardrails are preserved. It also correctly notes that other policy controls can further restrict access.

The card requires checking Step 1 console access/password availability before completing creation, instructs users to stop the IAM console-user path if unsupported, and keeps any actual creation/password/MFA actions user-operated. No access keys are proposed for browser viewing. The post-sign-in certificate check proves only that read operation, not deployment permission or resource existence.

## Failure paths and integration

Empty Copy permissions source list, boundary-only selection, unavailable console access and denied detail-page access each have an explicit explanation. The cross-links to the new card are present in the visual README and identity page. The builder is separately running the complete overlay validator and ZIP checks; those final packaging results are not claimed as independently executed here.

Official references independently checked:

- https://docs.aws.amazon.com/aws-managed-policy/latest/reference/ViewOnlyAccess.html
- https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSCertificateManagerReadOnly.html
- https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html

No blocking issue found in the new image or written guidance.
