import pytest

from app.file_validation import MAX_SIZE_BYTES, InvalidFileError, validate_file

JPEG_BYTES = b"\xff\xd8\xff" + b"\x00" * 20
PNG_BYTES = b"\x89PNG\r\n\x1a\n" + b"\x00" * 20
PDF_BYTES = b"%PDF-1.4\n" + b"\x00" * 20


def test_valid_jpeg_passes():
    validate_file("image/jpeg", JPEG_BYTES)


def test_valid_png_passes():
    validate_file("image/png", PNG_BYTES)


def test_valid_pdf_passes():
    validate_file("application/pdf", PDF_BYTES)


def test_unsupported_content_type_rejected():
    with pytest.raises(InvalidFileError, match="Unsupported content type"):
        validate_file("application/x-msdownload", b"MZ\x90\x00")


def test_spoofed_content_type_rejected():
    # Declares PDF but the bytes are actually a JPEG signature.
    with pytest.raises(InvalidFileError, match="does not match"):
        validate_file("application/pdf", JPEG_BYTES)


def test_oversized_file_rejected():
    oversized = b"\xff\xd8\xff" + b"\x00" * MAX_SIZE_BYTES
    with pytest.raises(InvalidFileError, match="exceeds"):
        validate_file("image/jpeg", oversized)
