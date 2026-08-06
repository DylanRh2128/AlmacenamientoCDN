import os
from datetime import datetime, timedelta, timezone

from botocore.signers import CloudFrontSigner
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

DEFAULT_EXPIRY_SECONDS = 600  # 10 minutes


def _rsa_signer(message: bytes, private_key_pem: bytes) -> bytes:
    private_key = load_pem_private_key(private_key_pem, password=None)
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())


def sign_url(url: str, key_pair_id: str, private_key_pem: bytes, expires_at: datetime) -> str:
    signer = CloudFrontSigner(key_pair_id, lambda message: _rsa_signer(message, private_key_pem))
    return signer.generate_presigned_url(url, date_less_than=expires_at)


def generate_download_url(s3_key: str, expires_in_seconds: int = DEFAULT_EXPIRY_SECONDS) -> str:
    url = f"https://{os.environ['CLOUDFRONT_DOMAIN']}/{s3_key}"
    private_key_pem = os.environ["CLOUDFRONT_PRIVATE_KEY"].encode().replace(b"\\n", b"\n")
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in_seconds)
    return sign_url(url, os.environ["CLOUDFRONT_KEY_PAIR_ID"], private_key_pem, expires_at)
