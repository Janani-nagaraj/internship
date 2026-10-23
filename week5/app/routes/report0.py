from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from auth import require_admin
from config import BUCKET_NAME
from database import register_candidate_owner
from storage import ensure_bucket, remove_objects_with_prefix, upload_bytes_to_minio
from utils import clean_candidate_id, originals_prefix, read_valid_image

router = APIRouter()


@router.post("/report-0")
async def report_0(
    candidate_id: str = Form(...),
    candidate_user_id: str = Form(...),
    degree_certificate: UploadFile = File(...),
    marksheet: UploadFile = File(...),
    user=Depends(require_admin),
):
    candidate_id = clean_candidate_id(candidate_id)

    candidate_user_id = candidate_user_id.strip()
    if not candidate_user_id:
        raise HTTPException(status_code=400, detail="Candidate Keycloak user ID is required.")

    try:
        register_candidate_owner(candidate_id, candidate_user_id)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not register candidate ownership in PostgreSQL: {exc}",
        )

    ensure_bucket()

    degree_ext, degree_content = await read_valid_image(degree_certificate)
    marksheet_ext, marksheet_content = await read_valid_image(marksheet)

    prefix = originals_prefix(candidate_id)

    try:
        remove_objects_with_prefix(prefix)

        degree_key = f"{prefix}degree_certificate{degree_ext}"
        marksheet_key = f"{prefix}marksheet{marksheet_ext}"

        upload_bytes_to_minio(degree_key, degree_content, "image/" + degree_ext.lstrip("."))
        upload_bytes_to_minio(marksheet_key, marksheet_content, "image/" + marksheet_ext.lstrip("."))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not save documents to MinIO: {exc}")

    return {
        "message": "Both documents uploaded successfully",
        "candidate_id": candidate_id,
        "storage": "MinIO",
        "bucket": BUCKET_NAME,
        "degree_certificate": degree_key,
        "marksheet": marksheet_key,
        "next_step": "Run POST /report-final with the same Candidate ID (using the candidate's token).",
    }
