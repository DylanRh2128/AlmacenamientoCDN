from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlparse

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from app.cloudfront_signer import sign_url


def _test_private_key_pem() -> bytes:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )


def test_signed_url_has_expected_query_params():
    private_key_pem = _test_private_key_pem()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

    url = sign_url(
        "https://example.cloudfront.net/some-key.jpg",
        key_pair_id="TESTKEYPAIRID",
        private_key_pem=private_key_pem,
        expires_at=expires_at,
    )

    query = parse_qs(urlparse(url).query)
    assert query["Key-Pair-Id"] == ["TESTKEYPAIRID"]
    assert "Signature" in query
    assert "Expires" in query
    assert int(query["Expires"][0]) > datetime.now(timezone.utc).timestamp()
