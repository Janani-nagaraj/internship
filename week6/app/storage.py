import io
from pathlib import Path

from fastapi import HTTPException
from minio import Minio

from config import (
    BUCKET_NAME, MINIO_ACCESS_KEY, MINIO_ENDPOINT, MINIO_SECRET_KEY, MINIO_SECURE,
)

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE,
)


def ensure_bucket():
    try:
        if not minio_client.bucket_exists(BUCKET_NAME):
            minio_client.make_bucket(BUCKET_NAME)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Cannot connect to MinIO: {exc}")


def remove_objects_with_prefix(prefix: str):
    for obj in minio_client.list_objects(BUCKET_NAME, prefix=prefix, recursive=True):
        minio_client.remove_object(BUCKET_NAME, obj.object_name)


def upload_bytes_to_minio(object_name: str, content: bytes, content_type: str):
    minio_client.put_object(
        bucket_name=BUCKET_NAME,
        object_name=object_name,
        data=io.BytesIO(content),
        length=len(content),
        content_type=content_type,
    )


def download_from_minio(object_name: str, destination: Path):
    response = None
    try:
        response = minio_client.get_object(BUCKET_NAME, object_name)
        destination.write_bytes(response.read())
    finally:
        if response is not None:
            response.close()
            response.release_conn()


def find_minio_document(prefix: str):
    objects = [
        obj.object_name
        for obj in minio_client.list_objects(BUCKET_NAME, prefix=prefix, recursive=True)
        if obj.object_name.startswith(prefix)
    ]
    if len(objects) != 1:
        return None
    return objects[0]
