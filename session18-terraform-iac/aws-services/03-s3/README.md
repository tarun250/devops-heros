# S3 — Simple Storage Service (Storage)

**What it is:** object storage. Practically unlimited size, 11 nines (99.999999999%) durability, accessed over HTTP(S). Not a filesystem — no real folders, just keys.

| Concept | Meaning |
|---|---|
| **Bucket** | container for objects; name is **globally unique**; lives in one region |
| **Object** | a file + metadata, identified by its **key** (`logs/2026/10/app.log`); up to 5 TB |
| **Prefix** | the folder-looking part of a key, used to group and filter |

## Storage classes

| Class | For | Retrieval |
|---|---|---|
| Standard | frequently accessed data | instant |
| Intelligent-Tiering | unknown or changing access | instant; moves data between tiers automatically |
| Standard-IA / One Zone-IA | infrequent access, cheaper storage | instant, with a retrieval fee |
| Glacier Instant / Flexible / Deep Archive | archives | milliseconds → minutes → up to 12 hours |

## Versioning

Keeps every version of an object. Overwrite = new version; delete = a delete marker (older versions are still there). Protects against accidental deletes and overwrites. Once enabled it can only be suspended, not switched off.

## Lifecycle policies

Rules that act on objects by age or prefix, e.g.:
- after 30 days → Standard-IA, after 90 days → Glacier
- delete `tmp/` objects after 7 days
- delete non-current versions after 60 days

## Encryption

- **At rest:** on by default (SSE-S3). Options: SSE-KMS (your KMS key, with an audit trail), SSE-C (you supply the key), or client-side encryption.
- **In transit:** HTTPS; enforce it with a bucket policy that denies `aws:SecureTransport = false`.

## Bucket policies

A JSON resource policy on the bucket (who can access it), evaluated together with IAM policies. **Block Public Access** is on by default — keep it on unless the bucket really must be public.

```json
{
  "Effect": "Deny",
  "Principal": "*",
  "Action": "s3:*",
  "Resource": ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/*"],
  "Condition": { "Bool": { "aws:SecureTransport": "false" } }
}
```

## Common use cases

- Backups and log archives.
- Static website hosting (with CloudFront).
- Data lake for analytics.
- Terraform remote state.
- CI/CD build artifacts.

My Terraform example: [`../../terraform-s3-demo`](../../terraform-s3-demo).
