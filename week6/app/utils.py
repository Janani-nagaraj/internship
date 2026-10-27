import io
import re
from pathlib import Path

from fastapi import HTTPException, UploadFile
from PIL import Image

from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE

CANDIDATE_ID_PATTERN = r"[A-Za-z0-9_-]{1,64}"


def clean_candidate_id(candidate_id: str) -> str:
    """Strip spaces and validate the candidate ID (used by both reports)."""
    candidate_id = candidate_id.strip()
    if not re.fullmatch(CANDIDATE_ID_PATTERN, candidate_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid Candidate ID. Use 1-64 letters, numbers, hyphens, or underscores.",
        )
    return candidate_id


def originals_prefix(candidate_id: str) -> str:
    """MinIO folder for a candidate's uploaded documents (same path for both reports)."""
    return f"candidates/{candidate_id}/originals/"


async def read_valid_image(upload: UploadFile):
    extension = Path(upload.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Upload PNG, JPG, JPEG, BMP, TIFF, or WEBP.")

    content = await upload.read()
    if not content:
        raise HTTPException(status_code=400, detail=f"{upload.filename} is empty.")
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Each document must be 15 MB or smaller.")

    try:
        with Image.open(io.BytesIO(content)) as image:
            image.verify()
    except Exception:
        raise HTTPException(status_code=400, detail=f"{upload.filename} is not a valid image.")

    return extension, content
