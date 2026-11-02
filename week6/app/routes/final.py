from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import FileResponse

from app.core.security import require_user
from app.core.config import TEMP_DIR
from app.db.ownership import ensure_candidate_owner
from app.services.ocr import extract_text_from_image
from app.services.pdf_report import build_report_pdf
from app.services.storage import download_from_minio, ensure_bucket, find_minio_document, upload_bytes_to_minio
from app.services.validation import clean_candidate_id, originals_prefix
from app.services.verification import documents_match

router = APIRouter()


@router.post("/report-final")
def report_final(
    candidate_id: str = Form(...),
    user=Depends(require_user),
):
    candidate_id = clean_candidate_id(candidate_id)

    try:
        ensure_candidate_owner(candidate_id, user["user_id"])
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database check failed: {exc}")

    ensure_bucket()

    prefix = originals_prefix(candidate_id)

    try:
        degree_key = find_minio_document(f"{prefix}degree_certificate")
        marksheet_key = find_minio_document(f"{prefix}marksheet")
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Could not retrieve documents from MinIO: {exc}")

    if not degree_key or not marksheet_key:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Documents not found for candidate {candidate_id}. "
                "Check the Candidate ID and upload both documents first."
            ),
        )

    degree_path = TEMP_DIR / f"{candidate_id}-degree{Path(degree_key).suffix}"
    marksheet_path = TEMP_DIR / f"{candidate_id}-marksheet{Path(marksheet_key).suffix}"
    pdf_path = TEMP_DIR / f"{candidate_id}-report-final-result.pdf"

    try:
        download_from_minio(degree_key, degree_path)
        download_from_minio(marksheet_key, marksheet_path)
        degree_text = extract_text_from_image(degree_path)
        marksheet_text = extract_text_from_image(marksheet_path)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Document download or OCR failed: {exc}")

    result = documents_match(degree_text, marksheet_text)

    try:
        build_report_pdf(pdf_path, degree_path, marksheet_path, result)
        upload_bytes_to_minio(
            f"candidates/{candidate_id}/reports/report-final-result.pdf",
            pdf_path.read_bytes(),
            "application/pdf",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not generate or store the PDF: {exc}")

    return FileResponse(
        path=str(pdf_path),
        media_type="application/pdf",
        filename=f"{candidate_id}-report-final-result.pdf",
    )
