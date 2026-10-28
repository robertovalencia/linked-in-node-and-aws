# AWS console screens, one concept at a time

[Visual guide](README.md) · [Sign-in and identity](01-sign-in-and-identity.md)

Every image on this page is an **official AWS example—not your AWS account**. Their visible resources belong to AWS tutorials. The images were inspected on 28 October 2026; source images span historical console versions, so use their fields to learn mechanisms rather than as exact current click instructions. This project's planned deployment differs where noted.

Images are embedded from verified official documentation/blog assets, including AWS's blog CDN. They require internet access even when reading the downloaded ZIP. Original source pages are linked beside each image. No image was generated, altered to resemble a deployed project or used as proof of current account state.

## 1 · VPC: see the network's relationships

![Official AWS console resource-map preview with public/private subnets, routes, internet gateway and S3 endpoint](https://docs.aws.amazon.com/images/vpc/latest/userguide/images/vpc-resource-map-update.PNG)

**Official AWS example—not your AWS account.** [Source and original-size image context](https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html). Current documentation; source image date unspecified. It is the VPC creation preview's resource-map view, not proof that its example was applied.

- **VPC:** the address-space boundary containing the displayed subnets.
- **Subnet/AZ:** placement within an Availability Zone. Public/private labels must be explained by routing and addressing, not their names alone.
- **Route connection:** the map joins subnets, route tables and destinations. This example includes an internet gateway and S3 gateway endpoint; it does **not** show a NAT gateway.

**Project connection:** [planned network.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/aws-ecs-dev/network.tf) defines a different topology with a selected NAT design. Follow the code's actual route targets. Study [47 · addressing](../generated/47-vpc-cidr-ipv6-and-subnet-design.md) and [49 · NAT/endpoints](../generated/49-private-connectivity-nat-and-endpoints.md).

**Recall:** Does calling a subnet “private” prove that it has no internet egress?

## 2 · Security groups: the source can be another group

![Official AWS security-group inbound-rule example showing another security group as the source for TCP 80](https://docs.aws.amazon.com/images/elasticbeanstalk/latest/dg/images/aeb-env-config-ec2-ec2console-sg-to-rule.png)

**Official AWS example—not your AWS account.** [Source](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.managing.ec2.instances.sg.html). This is an Elastic Beanstalk tutorial, not a service used by this project. The shared concept is an EC2/VPC security-group rule. The source image's arrow/highlight belongs to AWS.

- **Type/protocol/port:** what transport the rule permits. This example uses HTTP/TCP 80; that is not this project's approved client-facing HTTPS 443 rule.
- **Source group:** permits matching traffic from resources associated with that group under the applicable AWS rules; it is not a user's identity.
- **Direction:** an inbound rule belongs to its destination group. Do not attach a correct-looking rule to the wrong resource.

**Project connection:** read the proposed group/peer/port rules in [network.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/aws-ecs-dev/network.tf), [HTTPS ingress.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/aws-ecs-dev/ingress.tf) and [48 · SGs/NACLs](../generated/48-ingress-egress-security-groups-and-nacls.md). The actual client `/32` stays private. The screenshot's IDs and port are examples, not values to copy.

**Recall:** Why is ALB-group → application-port permission different from permitting that port from the entire internet?

## 3 · ECS: Running is not the whole health story

![Official AWS ECS Tasks tab with two Fargate tasks marked Running](https://d2908q01vomqb2.cloudfront.net/887309d048beef83ad3eabf2a79a64a389ab1c9f/2024/10/14/DBBLOG-4119-ecs2.png)

**Official AWS example—not your AWS account.** [2024 AWS Database Blog source](https://aws.amazon.com/blogs/database/build-containerized-applications-for-amazon-documentdb-that-run-on-amazon-ecs-on-aws-fargate/). The tutorial uses DocumentDB. Our project plans PostgreSQL on RDS; DocumentDB is not part of it. Open the original image to zoom into this compact screenshot.

- **Cluster:** organizes related ECS workloads.
- **Tasks / Running:** two task processes are running in this example.
- **FARGATE / health:** Fargate is the launch type; the pictured container health is Unknown. Running does not prove every health or business check passed.

**Project connection:** [compute.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/aws-ecs-dev/compute.tf) prepares tasks/services, but the reviewed infrastructure preview has zero application tasks/services activated. [53 · ECS](../generated/53-ecs-fargate-tasks-and-services.md) explains cluster, task and service separately.

**Recall:** Can an ECS task run while its load-balancer target is unhealthy?

## 4 · ECR: store and identify an image

![Official AWS ECR Images table with one tagged image and URI/digest columns](https://d2908q01vomqb2.cloudfront.net/887309d048beef83ad3eabf2a79a64a389ab1c9f/2024/10/14/DBBLOG-4119-docker-3.png)

**Official AWS example—not your AWS account.** [2024 AWS source](https://aws.amazon.com/blogs/database/build-containerized-applications-for-amazon-documentdb-that-run-on-amazon-ecs-on-aws-fargate/). Its example repository/tag are unrelated to this project's backend/frontend images; some identifiers are masked in the original.

- **Repository:** a collection of container images.
- **Tag:** a readable label such as `latest`; a label is not the immutable content identity.
- **Digest / pushed-at / size:** distinguish exact content from upload timing and storage size. Seeing an image here does not establish that a task uses it.

**Project connection:** [data.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/aws-ecs-dev/data.tf) and [the exact-source publisher](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/scripts/aws-ecs-publish-local.mjs) prepare repositories and reviewed image publication. Read [26 · images/ECR](../generated/26-aws-docker-and-ecr.md). Actual image publication remains a separate pending owner step in the recorded plan.

**Recall:** Why does the release manifest record a digest rather than relying only on a tag?

## 5 · ALB target groups: health has a specific meaning

![Official AWS target-group table showing Healthy targets and separate anomaly-detection results](https://d2908q01vomqb2.cloudfront.net/5b384ce32d8cdef02bc3a139d4cac0a22bb029e8/2023/11/21/ATW-1-target-group-with-anomaly.png)

**Official AWS example—not your AWS account.** [2023 AWS Networking Blog source](https://aws.amazon.com/blogs/networking-and-content-delivery/improving-availability-with-application-load-balancer-automatic-target-weights/). These are instance targets on port 80, not the project's proposed Fargate IP targets.

- **Registered target:** a destination associated with this target group.
- **Health status:** result of the configured load-balancer health-check mechanism.
- **Anomaly detection:** a separate signal. The pictured anomalous targets still show Healthy; do not rewrite one column's result as another's.

**Project connection:** [ingress.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/aws-ecs-dev/ingress.tf) connects listener, host routing and frontend target group. The project's preview initially has no application targets. Read [51 · ALB](../generated/51-alb-target-groups-and-health-checks.md) and the [pending rollout sequence](../walkthroughs/06-deployment-security-and-operations.md).

**Recall:** Why can a correct TLS listener return 503 before application activation?

## 6 · RDS: endpoint, network and lifecycle

![Official AWS RDS Connectivity and security details showing an endpoint, VPC and security-group links](https://docs.aws.amazon.com/images/hands-on/latest/amazon-rds-backup-restore-using-aws-backup/images/database-instance-details-page.png)

**Official AWS example—not your AWS account.** [AWS backup/restore tutorial source](https://aws.amazon.com/getting-started/hands-on/amazon-rds-backup-restore-using-aws-backup/). This older screenshot uses MySQL, a historical instance size and another Region. Our source plans PostgreSQL. The visible status is **Modifying**, not Available. Do not copy its sizing or infer readiness from the endpoint.

- **Endpoint:** DNS name clients use to reach the database.
- **VPC/security groups:** network placement and permission boundaries.
- **Status/engine:** lifecycle state and database technology; both matter when interpreting a screenshot.

**Project connection:** [data.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/aws-ecs-dev/data.tf) prepares the database. Application connections also need correct roles, pools and verified TLS in [compute.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/aws-ecs-dev/compute.tf). Study [57 · PostgreSQL/RDS recovery](../generated/57-rds-postgresql-backups-and-failover.md).

**Recall:** Does a valid endpoint prove that a private task can connect using its assigned database credentials?

## 7 · CloudWatch Logs: group → stream → events

![Official AWS CloudWatch log-events screen with timestamp/message columns, filters and time range](https://d2908q01vomqb2.cloudfront.net/972a67c48192728a34979d9a35164c1295401b71/2021/11/10/fig5sf.png)

**Official AWS example—not your AWS account.** [2021 AWS monitoring blog source](https://aws.amazon.com/blogs/mt/how-to-monitor-hybrid-environment-with-aws-services/). This example ingests on-premises system logs, not our ECS application logs. Modern navigation names can differ.

- **Log group:** organizes streams with group-level retention/access settings.
- **Log stream:** a sequence of events from a particular source.
- **Timestamp/message/filter/time range:** first check scope and time before concluding that a message is missing.

**Project connection:** [compute.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/aws-ecs-dev/compute.tf) prepares log groups and task log drivers; [observability.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/aws-ecs-dev/observability.tf) prepares metric alarms. This screenshot shows **log events, not an alarm configuration or notification delivery**. [65 · CloudWatch](../generated/65-cloudwatch-agent-logs-metrics-and-alarms.md) explains those separate mechanisms.

**Recall:** Why can a log group exist while no application logs appear in it?

## 8 · S3: a bucket contains objects

![Official AWS S3 Objects tab containing one example object](https://docs.aws.amazon.com/images/hands-on/latest/backup-files-to-amazon-s3/images/bucket-named-mysuperawsbucket-single-file.png)

**Official AWS example—not your AWS account.** [AWS tutorial source](https://docs.aws.amazon.com/hands-on/latest/backup-files-to-amazon-s3/backup-files-to-amazon-s3.html). Historical console image; it shows an example image object. Do not use this tutorial's old creation screens to infer today's encryption defaults.

- **Bucket:** the object-storage container.
- **Object key:** a name inside that bucket; it is not a local filesystem path.
- **Size/storage class:** describe a stored object's properties, not its access policy or full retained-version cost.

**Project connection:** [bootstrap/main.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/bootstrap/main.tf) prepares the private/versioned/encrypted state bucket; state is not a release image or a public learning attachment. The recorded bucket plan remains unapplied. Read [36 · state/backend bootstrap](../generated/36-terraform-state-locking-and-bootstrap.md).

**Recall:** Why must Terraform state objects stay private even though Terraform source is in GitHub?

## 9 · ACM: issued certificate and validation are separate fields

![Official AWS ACM example showing Issued status, successful DNS validation and the validation CNAME](https://docs.aws.amazon.com/images/acm/latest/userguide/images/Dns-renewal-2.png)

**Official AWS example—not your AWS account.** [AWS certificate documentation source](https://docs.aws.amazon.com/acm/latest/userguide/troubleshooting-renewal.html). The screenshot is historical, with a 2018 issuance date. Its example domain and CNAME must not be copied into your DNS zone.

- **Status:** the example certificate is Issued.
- **Domain validation / Success:** evidence of control of the named domain in that example.
- **CNAME Name/Type/Value:** the DNS proof record, different from the future application's traffic record.

**Project connection:** [certificate/main.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/aws-ecs-certificate/main.tf) requests the actual project certificate. Its [sanitized issuance receipt](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/docs/evidence/certificate-request/issuance.json) establishes our certificate's recorded status; this training image does not. [The DNS/TLS walkthrough](../walkthroughs/05-hostname-dns-and-certificate.md) explains that actual approved process. Browser capture of the signed-in project certificate will be added separately when authentication is complete.

**Recall:** Can an unused certificate be Issued while no application HTTPS endpoint exists?

## Screens not pictured here

No configured IAM permission policy, NAT gateway detail, MSK cluster, CloudWatch agent status or alarm notification is pictured. The conceptual lessons remain linked from the [full syllabus](../generated/44-cloud-complete-syllabus-and-mastery-map.md). A missing screenshot is not proof a feature exists or does not exist. MSK is an optional evaluated alternative; the selected prepared broker is Kafka on private EC2. Terraform is a CLI/source tool, not an AWS Console service; its actual runnable labs and expected output are in the [setup/process walkthrough](../walkthroughs/04-terraform-setup-and-plans.md).
