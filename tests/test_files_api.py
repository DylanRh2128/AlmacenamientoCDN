from unittest.mock import patch

from tests.conftest import API_KEY

HEADERS = {"X-API-Key": API_KEY}
JPEG_BYTES = b"\xff\xd8\xff" + b"\x00" * 20


def upload(client, content=JPEG_BYTES, content_type="image/jpeg", filename="photo.jpg"):
    return client.post(
        "/files", files={"file": (filename, content, content_type)}, headers=HEADERS
    )


def test_upload_happy_path(client):
    response = upload(client)
    assert response.status_code == 200
    body = response.json()
    assert body["original_filename"] == "photo.jpg"
    assert body["content_type"] == "image/jpeg"
    assert body["size_bytes"] == len(JPEG_BYTES)


def test_upload_invalid_content_type_returns_400(client):
    response = upload(client, content=b"MZ\x90\x00", content_type="application/x-msdownload")
    assert response.status_code == 400


def test_upload_without_api_key_returns_401(client):
    response = client.post("/files", files={"file": ("photo.jpg", JPEG_BYTES, "image/jpeg")})
    assert response.status_code == 401


def test_list_files(client):
    upload(client)
    response = client.get("/files", headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_download_url(client):
    created = upload(client).json()
    response = client.get(f"/files/{created['id']}/download-url", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["url"].startswith("https://fake.cdn/")


def test_get_download_url_not_found(client):
    response = client.get("/files/999/download-url", headers=HEADERS)
    assert response.status_code == 404


def test_delete_file(client):
    created = upload(client).json()

    with patch("app.files.delete_file") as mocked_delete:
        response = client.delete(f"/files/{created['id']}", headers=HEADERS)
        mocked_delete.assert_called_once()

    assert response.status_code == 204
    assert client.get(f"/files/{created['id']}/download-url", headers=HEADERS).status_code == 404


def test_delete_file_not_found(client):
    response = client.delete("/files/999", headers=HEADERS)
    assert response.status_code == 404
