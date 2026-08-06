import os

import boto3

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = boto3.client(
            "s3",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            region_name=os.environ["AWS_REGION"],
        )
    return _client


def upload_file(s3_key: str, content: bytes, content_type: str) -> None:
    _get_client().put_object(
        Bucket=os.environ["S3_BUCKET_NAME"],
        Key=s3_key,
        Body=content,
        ContentType=content_type,
    )


def delete_file(s3_key: str) -> None:
    _get_client().delete_object(Bucket=os.environ["S3_BUCKET_NAME"], Key=s3_key)
