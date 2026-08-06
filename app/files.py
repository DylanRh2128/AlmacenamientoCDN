import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.cloudfront_signer import DEFAULT_EXPIRY_SECONDS, generate_download_url
from app.db import get_db
from app.file_validation import EXTENSIONS, InvalidFileError, validate_file
from app.models import FileRecord
from app.s3_client import delete_file, upload_file
from app.schemas import DownloadUrlOut, FileOut

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.post("/files", response_model=FileOut)
async def create_file(file: UploadFile, db: Session = Depends(get_db)):
    content = await file.read()

    try:
        validate_file(file.content_type, content)
    except InvalidFileError as e:
        raise HTTPException(status_code=400, detail=str(e))

    s3_key = f"{uuid.uuid4()}{EXTENSIONS[file.content_type]}"

    try:
        upload_file(s3_key, content, file.content_type)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to upload to S3: {e}")

    record = FileRecord(
        s3_key=s3_key,
        original_filename=file.filename or s3_key,
        content_type=file.content_type,
        size_bytes=len(content),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/files", response_model=list[FileOut])
def list_files(db: Session = Depends(get_db)):
    return db.query(FileRecord).order_by(FileRecord.created_at.desc()).all()


@router.get("/files/{file_id}/download-url", response_model=DownloadUrlOut)
def get_download_url(file_id: int, db: Session = Depends(get_db)):
    record = db.get(FileRecord, file_id)
    if record is None:
        raise HTTPException(status_code=404, detail="File not found")

    url = generate_download_url(record.s3_key)
    return DownloadUrlOut(url=url, expires_in_seconds=DEFAULT_EXPIRY_SECONDS)


@router.delete("/files/{file_id}", status_code=204)
def delete_file_record(file_id: int, db: Session = Depends(get_db)):
    record = db.get(FileRecord, file_id)
    if record is None:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        delete_file(record.s3_key)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to delete from S3: {e}")

    db.delete(record)
    db.commit()
