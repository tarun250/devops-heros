variable "aws_region" {
  type        = string
  description = "AWS region for all resources."
  default     = "ap-south-1"
}

variable "project_name" {
  type        = string
  description = "Prefix used in resource names and tags."
  default     = "session19"
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the VPC."
  default     = "10.30.0.0/16"
}

variable "public_subnet_cidr" {
  type        = string
  description = "CIDR block for the public subnet (must be inside vpc_cidr)."
  default     = "10.30.1.0/24"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type (t3.micro is free-tier eligible)."
  default     = "t3.micro"
}

variable "allowed_ssh_cidr" {
  type        = string
  description = "Only this CIDR may SSH in. Set it to your own IP/32 — never 0.0.0.0/0."
  default     = "203.0.113.10/32"
}
