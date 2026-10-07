# Session 18 — Terraform & Infrastructure as Code (Submission)

Terraform v1.16.2, AWS provider `~> 6.0`, Windows / PowerShell.

> No AWS account/credentials on this machine, so `terraform plan` / `apply` were **not** run.
> All configs are formatted, initialised and validated.

## Terraform CLI

```powershell
terraform version
```
![Terraform version](./screenshots/01-terraform-version.png)

## S3 demo (`terraform-s3-demo/`)

| File | Purpose |
|---|---|
| `terraform.tf` | required Terraform + AWS provider versions |
| `providers.tf` | AWS provider, region from variable |
| `variables.tf` | `aws_region`, `bucket_name` |
| `main.tf` | `aws_s3_bucket` with tags, `force_destroy` |
| `outputs.tf` | bucket name, ARN, region |

```powershell
terraform fmt -check -recursive
terraform init
```
![fmt and init](./screenshots/02-s3-fmt-init.png)

```powershell
terraform validate
terraform providers
```
![validate](./screenshots/03-s3-validate.png)

To actually create it (needs `aws configure` first):
```powershell
terraform plan -var="bucket_name=<globally-unique-name>"
terraform apply -var="bucket_name=<globally-unique-name>"
terraform destroy
```

## All labs (01–09) validate

`init -backend=false` + `validate` in every lab folder:

![All labs validate](./screenshots/04-all-labs-validate.png)
