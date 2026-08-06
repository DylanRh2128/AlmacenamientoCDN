MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10MB

MAGIC_BYTES = {
    "image/jpeg": (b"\xff\xd8\xff",),
    "image/png": (b"\x89PNG\r\n\x1a\n",),
    "application/pdf": (b"%PDF-",),
}

EXTENSIONS = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "application/pdf": ".pdf",
}


class InvalidFileError(ValueError):
    pass


def validate_file(content_type: str, content: bytes) -> None:
    if content_type not in MAGIC_BYTES:
        raise InvalidFileError(
            f"Unsupported content type {content_type!r}. Allowed: {sorted(MAGIC_BYTES)}"
        )

    if len(content) > MAX_SIZE_BYTES:
        raise InvalidFileError(f"File exceeds the {MAX_SIZE_BYTES} byte limit")

    if not content.startswith(MAGIC_BYTES[content_type]):
        raise InvalidFileError(
            f"File content does not match the declared content type {content_type!r}"
        )
