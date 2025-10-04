variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "eu-central-1"
}

variable "app_name" {
  type        = string
  description = "Application name prefix"
  default     = "invoice-processing"
}

variable "db_password" {
  type        = string
  description = "RDS Postgres password"
  sensitive   = true
  default     = "change-db-password"
}

variable "ecr_image_tag" {
  type        = string
  description = "ECR image tag to deploy"
  default     = "latest"
}
