resource "aws_cloudwatch_log_group" "chpp_log_group" {
  name              = "/${var.project_name}/california-house-price-prediction"
  retention_in_days = var.log_retention_in_days
  kms_key_id        = aws_kms_key.logs.arn
}

resource "aws_cloudwatch_log_group" "vpc_flow_logs" {
  name              = "/${var.project_name}/vpc-flow-logs"
  retention_in_days = var.log_retention_in_days
  kms_key_id        = aws_kms_key.logs.arn
}

resource "aws_flow_log" "chpp_vpc" {
  vpc_id                   = aws_vpc.chpp_vpc.id
  traffic_type             = "ALL"
  log_destination_type     = "cloud-watch-logs"
  log_destination          = aws_cloudwatch_log_group.vpc_flow_logs.arn
  iam_role_arn             = aws_iam_role.vpc_flow_logs.arn
  max_aggregation_interval = 60

  tags = {
    Name = "${var.project_name}-vpc-flow-logs"
  }
}
