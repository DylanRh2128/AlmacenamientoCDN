# Security

## Secrets

All of `DATABASE_URL`, `API_KEY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`,
`CLOUDFRONT_PRIVATE_KEY`, and `CLOUDFRONT_KEY_PAIR_ID` are environment variables (`.env`,
git-ignored; only `.env.example` with placeholders is committed). `CLOUDFRONT_PRIVATE_KEY` is
the most sensitive value here — it's the RSA private key that lets anyone mint a valid signed
URL for any file in the bucket. Treat it exactly like a password, never paste it anywhere but
`.env` or your deployment platform's secret manager.

## One-time AWS setup checklist (not automated — done once, manually, in the AWS console/CLI)

1. **S3 bucket**: create it with **Block Public Access fully enabled**. This app never relies
   on the bucket being reachable directly.
2. **CloudFront distribution**: origin = the bucket, using **Origin Access Control (OAC)** —
   this is what lets CloudFront read the bucket while the bucket stays otherwise unreachable.
3. **CloudFront key pair + trusted key group**: generate an RSA key pair, upload the public key
   to CloudFront as a trusted key group attached to the distribution's cache behavior (set to
   require signed URLs), keep the private key for `CLOUDFRONT_PRIVATE_KEY`.
4. **IAM user with least privilege**: only `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject`,
   scoped to this one bucket's ARN — not a broad `AmazonS3FullAccess` policy. Its access
   key/secret become `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`.

## Two independent access barriers

Reaching a file's bytes requires *both* a valid `X-API-Key` (to call
`GET /files/{id}/download-url` in the first place) *and* the resulting signed URL not having
expired yet (10 minutes). Neither alone is enough.

## Input validation

`app/file_validation.py` checks both the declared `Content-Type` and the file's actual magic
bytes before anything touches S3 — see `docs/architecture.md` for why the header alone isn't
trusted. Server-generated `s3_key` values mean the user-supplied filename never becomes a
storage path.
