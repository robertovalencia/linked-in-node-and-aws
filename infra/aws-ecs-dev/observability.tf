locals {
  alarms = {
    broker_disk      = { namespace = "Marketplace/ECSDev", metric = "disk_used_percent", statistic = "Maximum", threshold = 80, comparison = "GreaterThanOrEqualToThreshold", dimensions = { InstanceId = aws_instance.broker.id } }
    broker_process   = { namespace = "Marketplace/ECSDev", metric = "procstat_lookup_pid_count", statistic = "Minimum", threshold = 1, comparison = "LessThanThreshold", dimensions = { InstanceId = aws_instance.broker.id } }
    alb_unhealthy    = { namespace = "AWS/ApplicationELB", metric = "UnHealthyHostCount", statistic = "Maximum", threshold = 0, comparison = "GreaterThanThreshold", dimensions = { LoadBalancer = aws_lb.dev.arn_suffix, TargetGroup = aws_lb_target_group.frontend.arn_suffix } }
    alb_5xx          = { namespace = "AWS/ApplicationELB", metric = "HTTPCode_ELB_5XX_Count", statistic = "Sum", threshold = 5, comparison = "GreaterThanOrEqualToThreshold", dimensions = { LoadBalancer = aws_lb.dev.arn_suffix } }
    database_storage = { namespace = "AWS/RDS", metric = "FreeStorageSpace", statistic = "Minimum", threshold = 2147483648, comparison = "LessThanThreshold", dimensions = { DBInstanceIdentifier = aws_db_instance.dev.identifier } }
    database_cpu     = { namespace = "AWS/RDS", metric = "CPUUtilization", statistic = "Average", threshold = 80, comparison = "GreaterThanThreshold", dimensions = { DBInstanceIdentifier = aws_db_instance.dev.identifier } }
    broker_status    = { namespace = "AWS/EC2", metric = "StatusCheckFailed", statistic = "Maximum", threshold = 0, comparison = "GreaterThanThreshold", dimensions = { InstanceId = aws_instance.broker.id } }
  }
}
resource "aws_cloudwatch_metric_alarm" "dev" {
  for_each            = local.alarms
  alarm_name          = "${local.name}-${each.key}"
  alarm_description   = "${var.notification_topic_arn == null ? "Notification destination pending; inspect CloudWatch" : "Owner-approved notification topic configured"}. Live metric/transition/delivery rehearsals remain required."
  namespace           = each.value.namespace
  metric_name         = each.value.metric
  statistic           = each.value.statistic
  threshold           = each.value.threshold
  comparison_operator = each.value.comparison
  dimensions          = each.value.dimensions
  period              = 60
  evaluation_periods  = 3
  datapoints_to_alarm = 2
  treat_missing_data  = contains(["broker_disk", "broker_process"], each.key) ? "breaching" : "notBreaching"
  alarm_actions       = var.notification_topic_arn == null ? [] : [var.notification_topic_arn]
  ok_actions          = var.notification_topic_arn == null ? [] : [var.notification_topic_arn]
}
