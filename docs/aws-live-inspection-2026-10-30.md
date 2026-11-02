# What to inspect in this AWS demo

Live metadata/metrics checked **October 30, 2026, 07:51 PM EDT**, account **772641336063**, **Ohio / us-east-2**. The infrastructure is provisioned; the marketplace application has not been activated. This guide uses the current ECS/RDS environment, not the separate historical EC2 app-deployment example.

## Start with these console pages

| Open | Find | What to inspect / current result |
|---|---|---|
| [EC2 instance](https://us-east-2.console.aws.amazon.com/ec2/home?region=us-east-2#InstanceDetails:instanceId=i-06a5a2da57b60f70a) | `linked-in-node-ecs-dev-broker` / `i-06a5a2da57b60f70a` | `m7i-flex.large`, **running**, system and instance checks **OK**, private/no public IP. This is the intended Kafka host; EC2 running does not prove Kafka process health. SSM is **Online**. |
| [RDS databases](https://us-east-2.console.aws.amazon.com/rds/home?region=us-east-2#databases:) | `linked-in-node-ecs-dev` | **available**, PostgreSQL **17.6**, `db.t4g.micro`. Open **Connectivity & security**, **Monitoring**, **Logs & events**, **Maintenance & backups**, and **Configuration**. |
| [CloudWatch alarms](https://us-east-2.console.aws.amazon.com/cloudwatch/home?region=us-east-2#alarmsV2:) | Names starting `linked-in-node-ecs-dev-` | Seven alarms: **five OK**, **two ALARM** (broker disk/process). No notification destination is configured. |
| [CloudWatch log groups](https://us-east-2.console.aws.amazon.com/cloudwatch/home?region=us-east-2#logsV2:log-groups) | Prefixes listed below | RDS has a stream. Broker and ECS log groups currently have no streams. A group existing is not proof of log emission. |
| [ECS cluster](https://us-east-2.console.aws.amazon.com/ecs/v2/clusters/linked-in-node-ecs-dev?region=us-east-2) | `linked-in-node-ecs-dev` | **0 services, 0 running tasks, 0 pending tasks**. There is no application container deployment to inspect yet. |
| [Load balancers](https://us-east-2.console.aws.amazon.com/ec2/home?region=us-east-2#LoadBalancers:) | `linked-in-node-ecs-dev` | **active**, HTTPS listener on443; target group has **0 targets**. Correct-host503 is the expected empty-target result. This is not a working app page. |
| [Operations bucket](https://s3.console.aws.amazon.com/s3/buckets/linked-in-node-ecs-dev-ops-82ee1eec1f5f1dccf0d365959f?region=us-east-2&tab=objects) | `alb/AWSLogs/772641336063/` | Logging test object and real `.log.gz` ALB access logs were verified in the preceding repair. This is not the protected Terraform state bucket. |

## 1. EC2: inspect the host without SSH

In EC2, select the instance → **Connect → Session Manager**. SSM metadata reports Online. The following CLI alternative requires the local Session Manager plugin; the browser option avoids that local plugin requirement:

```bash
aws --profile marketplace-dev --region us-east-2 ssm start-session \
  --target i-06a5a2da57b60f70a
```

Once you are **inside the EC2 session**, use these inspection commands:

```bash
uptime
df -h /
free -h
sudo systemctl is-active amazon-ssm-agent
sudo systemctl is-active docker
sudo systemctl is-active amazon-cloudwatch-agent
sudo docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

`is-active` may return a nonzero exit when a service is inactive; that is an observation, not an instruction to restart it. Kafka initialization waits for its separately approved broker-secret/bootstrap stage. Its process/container, agent emission and health are not yet verified. Do not paste environment dumps, container configuration or secret files into chat.

## 2. RDS: what to check first

Select `linked-in-node-ecs-dev`. Confirm:

- **Status:** available; **class:** db.t4g.micro; **engine:** PostgreSQL17.6.
- **Public access:** No. **Port:**5432. **Storage:**20GiB gp3, encrypted. **Deployment:**Single-AZ.
- **Deletion protection:** enabled. **Automated backup retention:**one day.
- **Parameter group:** `rds.force_ssl=1`, in-sync at the completion check.
- **Monitoring:** CPUUtilization, DatabaseConnections, FreeableMemory and FreeStorageSpace. A quiet instance does not prove application queries or migrations work.

Recent CloudWatch datapoints (each metric has its own timestamp):

| Metric | Latest sampled value |
|---|---:|
| RDS CPUUtilization | 4.47% |
| RDS DatabaseConnections | 0.0 |
| RDS FreeableMemory | 196.69 MiB |
| RDS FreeStorageSpace | 18.88 GiB |
| EC2 CPUUtilization | 0.90% |

RDS datapoints are around7:49–7:50PM EDT; the basic EC2 sample is around7:46PM. Values will move. The micro instance has1GiB total RAM; FreeableMemory is the reported available-memory metric, not installed RAM.

### Database connection: current boundary

Endpoint: `linked-in-node-ecs-dev.cnww62qusj03.us-east-2.rds.amazonaws.com`; port **5432**; initial database **postgres**; master username **marketplace_admin**. No password is included in this guide or was read for this inspection.

**A direct laptop connection will not work with the current private network.** The database allows PostgreSQL only from the four backend service security groups and the **bootstrap** security group. The existing EC2 broker's security group is **not allowed** to connect to5432; using it as an SSM database tunnel would still be blocked. Do not open the database publicly or add the broker as a shortcut.

The next actual SQL connection requires an authorized client inside the VPC using the existing bootstrap/service access path. That client has not been provisioned by this inspection. Database/application bootstrap was not run by this chat; the four capability schemas/roles are not claimed ready. SSM access to the broker is for host inspection and does not grant database access.

From such an approved VPC client, with `psql` and the Ohio RDS CA bundle available, the connection format is:

```bash
# Run on the approved VPC client, not directly on your laptop/broker.
# /path/to/rds-us-east-2-bundle.pem is the CA file on that client.
psql "host=linked-in-node-ecs-dev.cnww62qusj03.us-east-2.rds.amazonaws.com port=5432 dbname=postgres user=marketplace_admin sslmode=verify-full sslrootcert=/path/to/rds-us-east-2-bundle.pem" -W
```

The repository already contains the CA at `/Users/robertovalencia/Documents/Business/linked-in-node-and-aws/backend/certs/rds-us-east-2-bundle.pem` on your Mac. A VPC client needs its own copy/path. Obtain the administrator password privately from the RDS-linked managed secret in the console when you are ready; use the password prompt, not a password in a command, environment export or transcript. Use per-service users for later application traffic rather than the master account. [AWS RDS PostgreSQL TLS connection guidance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Concepts.General.SSL.html) explains certificate and hostname verification.

Safe checks once connected:

```sql
SELECT current_database(), current_user, version();
SHOW rds.force_ssl;
SELECT ssl, version, cipher FROM pg_stat_ssl WHERE pid = pg_backend_pid();
SELECT datname FROM pg_database WHERE NOT datistemplate ORDER BY datname;
```

In psql, `\conninfo`, `\l` and `\dt` show connection details, databases and tables. A successful login/TLS check still does not prove migrations, isolation, backup restoration or business acceptance.

## 3. CloudWatch: alarms, metrics and logs

Open **Alarms → All alarms**, filter `linked-in-node-ecs-dev-`. Current snapshot:

| Alarm suffix | State | What it watches |
|---|---|---|
| `broker_status` | OK | EC2 StatusCheckFailed |
| `database_cpu` | OK | RDS CPUUtilization |
| `database_storage` | OK | RDS FreeStorageSpace |
| `alb_5xx` | OK | ALB-generated5xx responses |
| `alb_unhealthy` | OK | UnHealthyHostCount; empty targets are not proof of healthy app targets |
| `broker_disk` | ALARM | `Marketplace/ECSDev` / disk_used_percent; missing data counts as breaching |
| `broker_process` | ALARM | `Marketplace/ECSDev` / procstat_lookup_pid_count; missing data counts as breaching |

The two broker custom metrics returned **no datapoints in the inspected20-minute interval**. Open each alarm's **History**, **State reason**, **Graphed metrics** and **Details**. The ALARM states are consistent with missing telemetry and the configured missing-data policy; they do **not** establish that the disk is full. Conversely, an OK alarm with `notBreaching` missing-data treatment does not establish a working service. The metric namespace, exact InstanceId/DBInstanceIdentifier/LoadBalancer dimensions and time range matter.

For metrics, use **All metrics → AWS/RDS → DBInstanceIdentifier**, **AWS/EC2 → Per-Instance Metrics**, **AWS/ApplicationELB**, and custom namespace **Marketplace/ECSDev** if it has received data. Use Ohio and a recent1-hour range. No new dashboard, metrics, alarm action or paid logging feature was enabled by this inspection.

Open **Logs → Log groups**:

- `/aws/rds/instance/linked-in-node-ecs-dev/postgresql` — currently one stream. Start here for actual database logs.
- `/ec2/linked-in-node-ecs-dev/broker` — currently no streams; future Kafka container logs.
- `/ecs/linked-in-node-ecs-dev/bootstrap` — currently no streams.
- `/ecs/linked-in-node-ecs-dev/identity`, `/catalog`, `/inquiries`, `/notifications`, `/frontend` under that same prefix — currently no streams because no tasks have been activated.

All eight groups retain logs for seven days. Choose a stream and a recent time range; an empty group has no events to query. Alarm notifications are unconfigured, so these alarms currently send no email/SNS notifications.

## 4. Copyable read-only CLI checks

Run these on your Mac using the existing authenticated `marketplace-dev` profile. In AWS CloudShell, use its console-provided credentials and omit `--profile marketplace-dev` unless you have explicitly configured that named profile there; do not copy credentials into CloudShell:

```bash
aws --profile marketplace-dev --region us-east-2 sts get-caller-identity

aws --profile marketplace-dev --region us-east-2 ec2 describe-instance-status \
  --instance-ids i-06a5a2da57b60f70a --include-all-instances

aws --profile marketplace-dev --region us-east-2 rds describe-db-instances \
  --db-instance-identifier linked-in-node-ecs-dev \
  --query 'DBInstances[0].{Status:DBInstanceStatus,Class:DBInstanceClass,Endpoint:Endpoint.Address,Port:Endpoint.Port,Public:PubliclyAccessible,Encrypted:StorageEncrypted,BackupDays:BackupRetentionPeriod,Protected:DeletionProtection}'

aws --profile marketplace-dev --region us-east-2 cloudwatch describe-alarms \
  --alarm-name-prefix linked-in-node-ecs-dev- \
  --query 'MetricAlarms[].{Name:AlarmName,State:StateValue,MissingData:TreatMissingData,Reason:StateReason}' \
  --output table

aws --profile marketplace-dev --region us-east-2 ecs describe-clusters \
  --clusters linked-in-node-ecs-dev \
  --query 'clusters[0].{Running:runningTasksCount,Pending:pendingTasksCount,Services:activeServicesCount}'

aws --profile marketplace-dev --region us-east-2 logs describe-log-streams \
  --log-group-name /aws/rds/instance/linked-in-node-ecs-dev/postgresql \
  --order-by LastEventTime --descending --limit 5
```

These do not read passwords, create resources, change security groups, apply Terraform or clean up resources. Session Manager opens a session only when you choose to run that separate command.

## Existing project documents

- `docs/aws-micro-completion-execution-2026-10-30.md` — current executed/verified infrastructure and limitations.
- `docs/aws-ecs-dev.md` — architecture and security boundaries; historical preparation sections are labeled as such.
- `docs/aws-operator-runbook-2026-10-29.md` — operator-assisted cleanup sequence; historical dates/plans are not current approval artifacts.
- `docs/nodejs-aws-study-path/generated/65-cloudwatch-agent-logs-metrics-and-alarms.md` — concepts and learning exercises.
- `docs/nodejs-aws-study-path/walkthroughs/06-deployment-security-and-operations.md` — what deployment and telemetry checks prove.

**Deadline:** today at **9:51PM EDT**. The cleanup-review window started at7:51PM. There is no automatic teardown; current cleanup-transition/destroy artifacts still require exact approval. This inspection changed no AWS resources.
