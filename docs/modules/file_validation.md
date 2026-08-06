# `app/file_validation.py`

Pure function `validate_file(content_type, content)` — no I/O. Rejects anything not in the
allowed JPEG/PNG/PDF set, anything over `MAX_SIZE_BYTES`, and anything whose actual bytes don't
start with the correct magic-byte signature for its declared `content_type`. Raises
`InvalidFileError` (caught in `app/files.py` and turned into a `400`).
