# Credentials come from `aws configure` / environment variables — never from this file.
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project   = var.project_name
      ManagedBy = "Terraform"
      Session   = "19"
    }
  }
}
