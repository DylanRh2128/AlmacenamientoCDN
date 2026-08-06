# `app/files.py`

The API layer, all behind `verify_api_key` at the router level. `create_file` chains
`file_validation` → `s3_client.upload_file` → persists `FileRecord`, in that order, so nothing
gets written to the database for a file that was never actually stored. `delete_file_record`
deletes from S3 before deleting the metadata row, for the same reason in reverse — a failed S3
delete leaves the metadata behind rather than losing track of an orphaned object.
