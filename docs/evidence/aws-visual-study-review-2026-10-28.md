# Independent AWS visual study review

**Verdict: PASS for the prepared visual learning guide.** Reviewed 2026-10-28. This is a documentation and packaging verdict, not approval or verification of AWS provisioning, identity creation, or deployment.

## Actual review performed

- Read source AGENTS.md, ZIP builder, curriculum checker, all three final visual guides, image provenance manifest, root/study/walkthrough navigation additions, source Terraform/publisher references, actual certificate issuance receipt, and dated HTTPS plan review.
- Independently opened and visually inspected the local blank sign-in screenshot and all nine exact remote screenshot assets using the background browser. No remote media was downloaded, no image was generated or edited, and no AWS mutation was performed during this review.
- Independently opened every official source page and checked its rendered image DOM. All nine exact embedded asset URLs occur on their stated official AWS documentation/blog source page, including the blog CDN URLs.
- Checked the IAM console-user limitation, project/team access model, and invitation permission impact against current official AWS documentation: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html , https://docs.aws.amazon.com/accounts/latest/reference/sign-up-for-aws.html , and https://docs.aws.amazon.com/accounts/latest/reference/invite-team-members.html . The guidance matches those sources. The CLI role session correctly remains evidence of role credentials, not proof of the human login provider.

## Image and caption results

| Image | Independent observation and caption assessment |
|---|---|
| Actual sign-in | Email field blank; provider buttons, IAM user option and Sign up visible. No entered credential, private account menu, client CIDR or unrelated browser content. Correctly labeled unsigned-in entry screen. |
| VPC | Public/private subnet/resource map, route tables, internet gateway and S3 endpoint visible. No NAT depicted. Creation-preview and non-project limits preserved. |
| Security groups | HTTP/TCP 80 inbound source is a security group, with AWS's original arrow/highlight. Beanstalk source and different project HTTPS rule explicitly distinguished. |
| ECS | Two Fargate tasks show Running; container health is Unknown. Caption preserves that distinction and identifies DocumentDB sample versus planned PostgreSQL. Small source dimensions acknowledged. |
| ECR | One tagged image, upload time, size, URI/digest columns and original masked identifier visible. Caption does not claim workload deployment. |
| ALB | Targets show Healthy while a subset is separately Anomalous. Health checks distinguished from anomaly detection; instance targets distinguished from project IP targets. |
| RDS | MySQL, Modifying lifecycle, endpoint and VPC/security-group links visible. Historical sizing/Region and planned PostgreSQL differences clearly stated. |
| CloudWatch | Log group/stream/event hierarchy, timestamps/messages and filter/time selector visible. No claim of alarm configuration or notification delivery. |
| S3 | Bucket Objects tab and one example object visible. No inference about bucket policy, versioning, current encryption defaults or project state creation. |
| ACM | Historical example Issued status, DNS validation Success and CNAME visible. Not passed off as actual project certificate or application HTTPS evidence. |

Each service card explicitly labels the official AWS example as unrelated to the user's account, links its original source, names relevant fields in short explanations, connects to project code/lessons, and includes a recall question. Remote image dependence is disclosed on the overview and service page. Missing configured IAM/NAT/MSK/agent/alarm screenshots and the pending actual ACM capture are openly identified.

## Security, contracts and failure paths

No credentials, entered email, exact approved client address or unrelated browser content were found in the included images. The account ID and role name in the explanation are identifiers, not credentials. Source plan/issuance evidence supports the stated distinction: certificate issued and unused; five-create state bootstrap and 111-create HTTPS preview unapplied; application activation and HTTPS behavior unverified. The guide does not authorize service/user creation, invitations, policy attachment, plan application or paid API usage.

Project connections match inspected source: zonal NAT and S3 endpoint, security-group peer rules, PostgreSQL RDS, ECR repositories, IP target group and HTTPS listener, logs/alarms, protected state bucket, and certificate request. A Running task, stored image, database endpoint, issued certificate or log group is not described as proving the complete application healthy. Reviewing account/Region/filter/time before interpreting lists is appropriate.

## Largest gap and repair

The first staged version had no image cards, the ZIP builder omitted visuals, and the checker did not scan visual Markdown. These were repaired. A later review found relative code/evidence links escaping the standalone ZIP. The builder repaired them to verified pinned GitHub source links while retaining local study navigation, and repaired the same existing portability defect in affected walkthroughs.

I independently scanned the final archive's three visual Markdown files: **zero broken local targets**, 15 pinned project source links, and nine remote image links. The packaged blank screenshot SHA-256 is `686d875b97a2f5a098475071343622c5956aa0563fa48ca4a1f0666c57c9b020`, matching provenance. The archive contains five visual members (three Markdown, one provenance JSON, one PNG) among 128 managed members.

Independently reran the final updated curriculum checker against the complete staged overlay and actual source checkout: **PASS: 84 lessons, 64 cloud lessons, 321 mapped concepts, 627 local links, 230 pinned source references, 31 exact historical excerpts**. No reduced gate was used. Inspected the preventive guard: every local target must resolve inside the downloadable pack before its existence is accepted. The old repository fallback was removed, preventing existing files outside the package from masking broken standalone ZIP links. The builder separately reported an outside-pack negative fixture was rejected and then restored.

## Evidence limits and handoff

Actual signed-in ACM/service console screenshots remain pending user authentication. The prepared guide passes as a clearly labeled official-example learning guide with one actual unsigned-in sign-in capture. It must not be reported as nine screenshots of the user's deployed services.

At the final reread, image-provenance.json correctly records that the independent critic inspected every image and its official source DOM on 2026-10-28. The builder will record the largest gap/repair in docs/reviews.md before publication. Substantive verdict remains PASS.
