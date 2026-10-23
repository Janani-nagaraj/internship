import os
from pathlib import Path

import pytesseract

# ---------- Keycloak ----------
KEYCLOAK_ISSUER = os.getenv("KEYCLOAK_ISSUER", "http://localhost:8080/realms/capstone")
KEYCLOAK_JWKS_URL = os.getenv(
    "KEYCLOAK_JWKS_URL",
    "http://keycloak:8080/realms/capstone/protocol/openid-connect/certs",
)

# ---------- PostgreSQL ----------
DATABASE_URL = os.getenv("DATABASE_URL", "")

# ---------- MinIO ----------
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin123")
MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() == "true"
BUCKET_NAME = "document-verification"

# ---------- Folders ----------
BASE_DIR = Path(os.getenv("BASE_DIR", Path(__file__).resolve().parent.parent))
TEMP_DIR = BASE_DIR / "temporary"
REPORT_DIR = BASE_DIR / "reports"
TEMP_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ---------- Upload rules ----------
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"}
MAX_FILE_SIZE = 15 * 1024 * 1024

# ---------- Tesseract ----------
# Windows default for local VS Code runs; plain "tesseract" inside Docker/Linux.
pytesseract.pytesseract.tesseract_cmd = os.getenv(
    "TESSERACT_CMD",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe" if os.name == "nt" else "tesseract",
)
