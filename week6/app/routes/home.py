from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Document Verification API is running",
        "storage": "MinIO",
        "report_0": "/report-0",
        "report_final": "/report-final",
        "instructions": (
            "Upload both documents through Report 0, "
            "then run Report Final without uploading again."
        ),
    }
