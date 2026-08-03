variable "project_name" {
  description = "Project name used for resource naming and tags."
  type        = string
  default     = "devops-learning"
}

variable "allowed_ingress_cidr" {
  description = "CIDR block allowed to reach the load balancer. Restrict to your IP."
  type        = string
  default     = "0.0.0.0/0"
}

variable "log_retention_in_days" {
  description = "CloudWatch log retention period."
  type        = number
  default     = 30
}

variable "aws_region" {
  description = "AWS region for all resources."
  type        = string
  default     = "eu-north-1"
}

variable "ecs_task_cpu" {
  description = "CPU units for the ECS task."
  type        = number
  default     = 512
}

variable "ecs_task_memory" {
  description = "Memory (in MiB) for the ECS task."
  type        = number
  default     = 1024
}

variable "demo_container_port" {
  description = "Port for the demo container."
  type        = number
}

variable "api_container_port" {
  description = "Port for the API container."
  type        = number
}

variable "model_path" {
  description = "Path to the model file used by the API container."
  type        = string
}
