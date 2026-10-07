# IAM — Identity and Access Management (Governance)

**What it is:** the AWS service that controls **who** can do **what** on **which** resources. Global (not per region), free.

| Concept | Meaning |
|---|---|
| **User** | one person or app with long-term credentials (console password and/or access keys) |
| **Group** | a set of users; attach policies once and every member gets them (`developers`, `admins`) |
| **Role** | an identity with **no** long-term credentials; assumed temporarily by a service (EC2, Lambda), another account, or a federated user (SSO, GitHub OIDC) |
| **Policy** | JSON document listing allowed/denied actions on resources |
| **Permission** | the effective result of all policies that apply to an identity |

Example policy — read-only access to one bucket:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject", "s3:ListBucket"],
    "Resource": ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/*"]
  }]
}
```

How AWS decides: everything is **denied by default** → an explicit `Allow` grants it → an explicit `Deny` always wins.

Policy types: AWS-managed (`ReadOnlyAccess`), customer-managed (yours, reusable), inline (attached to one identity only).

## Least privilege

Give only the actions and resources needed for the job, nothing more. Start narrow and widen only when something is actually blocked. IAM Access Analyzer can generate a policy from what was really used.

## Best practices

- Don't use the **root** account day to day; turn on MFA for it and don't create root access keys.
- MFA for every human user.
- Prefer **roles** over access keys (EC2 instance profile, GitHub Actions OIDC instead of storing keys as secrets).
- Attach permissions to **groups**, not individual users.
- Rotate or delete unused access keys; never commit them to Git.
- Use IAM Identity Center (SSO) when there are many users or accounts.

## Common use cases

- EC2 instance reading from S3 through an instance **role**.
- CI/CD pipeline deploying with a role assumed via OIDC.
- Read-only auditors group.
- Terraform running with a dedicated deploy role.
