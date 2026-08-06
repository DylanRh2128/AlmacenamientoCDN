# API Reference

All endpoints require header `X-API-Key` matching the server's `API_KEY` (`401` if missing or
wrong).

## `POST /files`

`multipart/form-data`, field `file`. Allowed content types: `image/jpeg`, `image/png`,
`application/pdf`. Max size: 10MB.

Response `200`:
```json
{
  "id": 1,
  "created_at": "2026-08-05T12:00:00",
  "original_filename": "photo.jpg",
  "content_type": "image/jpeg",
  "size_bytes": 245312
}
```

Errors: `400` if the content type is unsupported, too large, or the bytes don't match the
declared type. `502` if the S3 upload fails.

## `GET /files`

Lists file metadata, most recent first. Never includes a download URL — request one explicitly.

## `GET /files/{id}/download-url`

```json
{"url": "https://your-distribution.cloudfront.net/...&Expires=...&Signature=...&Key-Pair-Id=...", "expires_in_seconds": 600}
```

`404` if the file doesn't exist.

## `DELETE /files/{id}`

`204` on success. `404` if the file doesn't exist. `502` if the S3 deletion fails (metadata is
kept in that case, so the file isn't lost track of).
