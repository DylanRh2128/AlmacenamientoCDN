# `app/cloudfront_signer.py`

`sign_url()` is the pure, testable core: given a URL, a key pair ID, a private key (PEM bytes),
and an expiry `datetime`, it returns a CloudFront-signed URL using `botocore`'s
`CloudFrontSigner` with RSA-SHA1 signing (`cryptography`). `generate_download_url()` is the thin
wrapper that reads `CLOUDFRONT_DOMAIN`/`CLOUDFRONT_KEY_PAIR_ID`/`CLOUDFRONT_PRIVATE_KEY` from the
environment and calls it for a given `s3_key`. Tests exercise `sign_url()` directly with a
throwaway in-memory key pair — never a real credential.
