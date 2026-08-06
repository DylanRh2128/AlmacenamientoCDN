# Data Model

## `files`

| column            | type      | notes                                            |
|-------------------|-----------|---------------------------------------------------|
| id                | int, PK   |                                                   |
| created_at        | datetime  | defaults to now (UTC)                            |
| s3_key            | string    | unique, server-generated (`uuid4()` + extension)  |
| original_filename | string    | display only, never used to build the S3 path     |
| content_type      | string    | one of: image/jpeg, image/png, application/pdf    |
| size_bytes        | bigint    |                                                   |

Single table — the actual file bytes live in S3, this table only tracks metadata.
`s3_key` is intentionally excluded from the API responses (see `app/schemas.py`'s `FileOut`) —
clients only ever get a signed download URL, never the raw storage key.
