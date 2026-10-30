variable "region" {
  type    = string
  default = "us-east-2"
  validation {
    condition     = var.region == "us-east-2"
    error_message = "This reviewed lab and its prices are scoped to Ohio/us-east-2."
  }
}
variable "project" {
  type    = string
  default = "linked-in-node"
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,18}$", var.project))
    error_message = "Use a lowercase project slug of 3-19 characters."
  }
}
variable "owner" {
  type        = string
  description = "Human accountable for the 24-hour deployment and teardown."
}
variable "expires_at" {
  type        = string
  description = "Reviewed UTC RFC3339 teardown deadline. This tag does not schedule deletion."
  validation {
    condition     = can(formatdate("YYYY-MM-DD", var.expires_at))
    error_message = "Provide an RFC3339 UTC deadline."
  }
}
variable "approved_client_cidrs" {
  type        = set(string)
  default     = []
  nullable    = false
  description = "Explicit approved IPv4 client networks. No default and no Internet-wide ranges."
  validation {
    condition     = (!var.deploy_application || length(var.approved_client_cidrs) > 0) && alltrue([for c in var.approved_client_cidrs : can(cidrnetmask(c)) && try(tonumber(split("/", c)[1]) >= 24, false)])
    error_message = "Use explicit IPv4 /24 or narrower client networks; 0.0.0.0/0 is forbidden."
  }
}
variable "certificate_arn" {
  type        = string
  default     = null
  description = "Owner-validated ISSUED ACM public certificate in us-east-2. Terraform does not create domains or certificates."
  validation {
    condition     = var.certificate_arn == null ? !var.deploy_application : can(regex("^arn:aws:acm:us-east-2:[0-9]{12}:certificate/[a-f0-9-]+$", var.certificate_arn))
    error_message = "Supply an existing Ohio ACM certificate ARN."
  }
}
variable "application_hostname" {
  type        = string
  default     = null
  description = "Owner-controlled DNS hostname covered by certificate_arn; owner points it at the ALB after approval."
  validation {
    condition     = var.application_hostname == null ? !var.deploy_application : can(regex("^[a-z0-9][a-z0-9.-]+\\.[a-z]{2,}$", var.application_hostname))
    error_message = "Provide a DNS hostname. .invalid is reserved for mock tests only."
  }
}
variable "deploy_application" {
  type        = bool
  default     = false
  description = "False: infrastructure review/staging only, services have desired count zero. True requires verified images, migration and runtime-secret setup."
}
variable "teardown_discard_demo_data" {
  type        = bool
  default     = false
  nullable    = false
  description = "Explicit teardown-only choice to discard synthetic demo data after stopping application services. A separately reviewed transition must be applied before destroy; it does not delete resources or retained state by itself."
  validation {
    condition     = !var.teardown_discard_demo_data || !var.deploy_application
    error_message = "Discarding demo data is allowed only with deploy_application=false; stop application services before teardown."
  }
}
variable "image_digests" {
  type        = object({ backend = string, frontend = string })
  default     = null
  description = "Verified immutable sha256 digests in this root's ECR repositories. Required to activate application or register migration tasks."
  validation {
    condition     = var.image_digests == null ? !var.deploy_application : alltrue([for d in values(var.image_digests) : can(regex("^sha256:[a-f0-9]{64}$", d))])
    error_message = "Activation requires verified sha256 image digests; tags/latest are forbidden."
  }
}
variable "broker_ami_id" {
  type        = string
  default     = null
  description = "Optional reviewed broker AMI pin. Null follows the AL2023 SSM image parameter; pin the deployed AMI during repair to preserve the host/data volume. AMI changes still require a reviewed replacement plan."
  validation {
    condition     = var.broker_ami_id == null ? true : can(regex("^ami-[a-f0-9]{17}$", var.broker_ami_id))
    error_message = "Provide a reviewed ami- followed by 17 lowercase hexadecimal digits, or null to use AL2023 SSM discovery."
  }
}
variable "kafka_image" {
  type        = string
  description = "Verified immutable apache/kafka image reference (linux/amd64), apache/kafka:VERSION@sha256:DIGEST."
  validation {
    condition     = can(regex("^apache/kafka:[0-9.]+@sha256:[a-f0-9]{64}$", var.kafka_image))
    error_message = "Pin the broker version and verified SHA256 image digest."
  }
}
variable "rds_backup_retention_days" {
  type        = number
  default     = 7
  nullable    = false
  description = "Seven-day ordinary recovery default. One day is an explicit Free-plan demo candidate, not proof the account permits RDS creation; disabling backups is forbidden."
  validation {
    condition     = contains([1, 7], var.rds_backup_retention_days)
    error_message = "Use the reviewed seven-day default or explicit one-day demo candidate; zero/unreviewed retention is forbidden."
  }
}
variable "postgres_engine_version" {
  type        = string
  default     = "17"
  description = "Supported PostgreSQL 17 major/minor, checked against Ohio orderable versions before apply."
  validation {
    condition     = can(regex("^17(\\.[0-9]+)?$", var.postgres_engine_version))
    error_message = "This parameter group and tested database contract require PostgreSQL 17."
  }
}
variable "protect_database" {
  type        = bool
  default     = true
  description = "Deletion protection. Removing this requires a separately reviewed teardown plan and retained final snapshot."
}
variable "recovery_snapshot_suffix" {
  type        = string
  description = "Unique final-snapshot suffix, e.g. review-20261027. Snapshot retention remains billable after destroy."
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{1,30}$", var.recovery_snapshot_suffix))
    error_message = "Use a unique lowercase snapshot suffix beginning with a letter."
  }
}
variable "notification_topic_arn" {
  type        = string
  default     = null
  description = "Optional pre-existing owner-approved Ohio SNS topic for alarm/OK events. Null prepares alarms without delivering notifications; no topic/contact is created."
  validation {
    condition     = var.notification_topic_arn == null ? true : can(regex("^arn:aws:sns:us-east-2:[0-9]{12}:[A-Za-z0-9_-]+$", var.notification_topic_arn))
    error_message = "Use a pre-existing Ohio SNS topic ARN or null."
  }
}
variable "seed_demo" {
  type        = bool
  default     = false
  description = "Explicit opt-in to synthetic demo accounts/profiles for the CIDR-restricted 24-hour interview lab. Never enable for real user data."
}
