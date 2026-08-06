# `app/s3_client.py`

Thin wrapper around `boto3`'s S3 client: `upload_file(s3_key, content, content_type)` and
`delete_file(s3_key)`. The client is created lazily (module-level singleton) so importing this
module never requires AWS credentials — only calling one of these two functions does.
