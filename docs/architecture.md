# Architecture

## Flow

`POST /files` → `app/file_validation.py` checks declared type + magic bytes + size →
`app/s3_client.py` uploads to the private bucket under a server-generated key →
`app/models.py`'s `FileRecord` is persisted. `GET /files/{id}/download-url` →
`app/cloudfront_signer.py` builds a signed URL good for 10 minutes. `DELETE /files/{id}` removes
the S3 object first, then the metadata row — if S3 deletion fails, the metadata stays so the
file isn't silently orphaned.

## Why AWS S3 + CloudFront, not Cloudflare R2

R2 is genuinely simpler (S3-compatible API, no egress fees, CDN built in) and would have been
the pragmatic pick for a fully hands-off portfolio piece. AWS S3 + CloudFront was chosen
instead because it's the combination most freelance clients specifically ask for by name, and it
demonstrates handling more real AWS pieces: IAM least-privilege credentials, S3 bucket policies,
and CloudFront signed URLs with a trusted key pair — skills that transfer directly to client work
built on AWS.

## Why nothing is public

Every endpoint (`POST /files`, `GET /files`, `GET /files/{id}/download-url`, `DELETE /files/{id}`)
requires `X-API-Key`. The S3 bucket blocks all public access; CloudFront reaches it only through
Origin Access Control, never directly. The only way to actually read file bytes is a signed
CloudFront URL, which only `GET /files/{id}/download-url` can produce — and that endpoint is
itself behind the API key. Two independent barriers, not one.

## Magic-byte validation, not just `Content-Type`

`app/file_validation.py` checks the first bytes of the uploaded content against the known
signatures for JPEG/PNG/PDF, in addition to the declared `Content-Type`. A client can set any
`Content-Type` header it wants — trusting it alone would let someone upload, say, an executable
labeled as a PDF. This is the junior-acceptable-vs-senior line for this project: junior-acceptable
is trusting the header; a senior validates what the bytes actually are.

## Server-generated storage keys

`s3_key` is always a fresh `uuid4()` plus the correct extension for the validated content type —
never derived from the user-supplied filename. Using an attacker-controlled filename as a
storage path risks collisions and path-traversal-style tricks; the original filename is kept
only as display metadata (`original_filename`), never used to build a path.

## Junior-acceptable vs. what a senior would do differently

- **Schema management**: `Base.metadata.create_all()` on startup, no Alembic — same tradeoff as
  the other projects in this portfolio.
- **Single API key for every operation**: fine for one API consumer (this portfolio demo); a
  senior serving multiple clients would issue per-client keys so access can be scoped/revoked
  individually.
- **10-minute signed URL expiry is a fixed constant**: reasonable default; a senior might make it
  configurable per file sensitivity (shorter for something highly confidential).
- **No malware scanning**: content-type/magic-byte validation stops type spoofing, not a
  malicious but genuinely valid PDF/image (e.g. an exploit embedded in a crafted PDF). A senior
  handling public uploads at scale would add a scanning step (e.g. ClamAV) before serving files
  back out.
