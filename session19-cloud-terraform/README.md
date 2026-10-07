# Session 19 — Cloud & Terraform in Action (Submission)

> No AWS account/credentials on this machine (AWS CLI not installed), so `plan` / `apply` / `destroy` were **not** run.
> All Terraform code is formatted, initialised and validated.

## Mini project — VPC with Terraform (`08-mini-project/`)

What it builds:

| Resource | Purpose |
|---|---|
| `aws_vpc.main` | the private network (CIDR from variable) |
| `aws_subnet.public` | public subnet in one AZ, auto-assign public IP |
| `aws_internet_gateway.main` | lets the VPC reach the internet |
| `aws_route_table.public` + association | `0.0.0.0/0 → IGW` for the public subnet |
| `aws_security_group.web` | HTTP 80 inbound, all outbound |

```powershell
terraform fmt -check
terraform init
```
![fmt and init](./screenshots/01-mini-fmt-init.png)

```powershell
terraform validate
```
![validate](./screenshots/02-mini-validate.png)

Resources, outputs and variables in the config:

![resources](./screenshots/03-mini-resources.png)

## All Terraform folders validate

`06-terraform-vpc`, `07-terraform-workflow` (S3), `08-mini-project`:

![validate all](./screenshots/04-vpc-workflow-validate.png)

To run for real (after `aws configure`):
```powershell
terraform plan
terraform apply
terraform output
terraform state list
terraform destroy
```

## EC2 extension questions

1. **Subnet?** The public subnet — it has the route to the IGW.
2. **Security group?** `web` SG (port 80 in).
3. **Why IGW route?** Without `0.0.0.0/0 → IGW` the subnet has no path to the internet, so it isn't really public.
4. **What else for reachability?** A public IP (auto-assign or Elastic IP), SG/NACL allowing the port, and the app listening on it.
5. **Why not SSH from `0.0.0.0/0`?** Anyone can brute-force port 22. Allow only your IP, or use SSM Session Manager.
