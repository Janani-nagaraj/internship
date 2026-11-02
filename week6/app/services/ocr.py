import re
from pathlib import Path

import pytesseract
from PIL import Image, ImageEnhance, ImageOps


def extract_text_from_image(image_path: Path) -> str:
    """Run OCR on the original image and enhanced variants, then combine the results."""
    with Image.open(image_path) as original:
        image = ImageOps.exif_transpose(original).convert("RGB")

    if image.width < 1800:
        scale = 1800 / image.width
        image = image.resize((1800, int(image.height * scale)), Image.Resampling.LANCZOS)

    gray = ImageOps.grayscale(image)
    gray = ImageOps.autocontrast(gray)
    gray = ImageEnhance.Contrast(gray).enhance(1.5)
    thresholded = gray.point(lambda pixel: 255 if pixel > 165 else 0)

    results = []
    for variant in [image, gray, thresholded]:
        for page_mode in (6, 11):
            try:
                text = pytesseract.image_to_string(variant, config=f"--oem 3 --psm {page_mode}")
                if text.strip():
                    results.append(text.strip())
            except Exception:
                continue

    if not results:
        raise RuntimeError(
            "Tesseract could not extract text. Check its installation and TESSERACT_CMD setting."
        )
    return "\n".join(results)


def clean_ocr_value(value: str) -> str:
    if not value:
        return ""

    value = value.replace("|", "I")
    value = re.sub(r"\s+", " ", value).strip()

    noise_words = r"\b(?:DOCUMENT|SPECIMEN|SAMPLE|UNIVERSITY|CONTROLLER|EXAMINATIONS|SIGNATURE)\b"
    value = re.sub(noise_words, " ", value, flags=re.IGNORECASE)

    stop_labels = (
        r"\b(?:register\s*(?:no|number)|reg\s*(?:no|number)|"
        r"roll\s*(?:no|number)|date\s+of\s+issue|"
        r"certificate\s+no|programme\s+period|"
        r"programme|program|class|result|percentage|"
        r"cgpa|subject|marks)\b"
    )
    value = re.split(stop_labels, value, maxsplit=1, flags=re.IGNORECASE)[0]

    value = re.sub(r"[^A-Za-z\s.'-]", " ", value)
    value = re.sub(r"\s+", " ", value).strip(" .'-")

    value = re.sub(
        r"^(?:(?:of|the|name|candidate|student)\s+)+", "", value, flags=re.IGNORECASE
    ).strip()

    if len(re.sub(r"[^A-Za-z]", "", value)) < 2:
        return ""
    return value


def extract_candidate_name(text: str):
    """Handles layouts like 'Name of Candidate: X', 'Candidate Name: X', 'This is to certify that X'."""
    lines = [
        re.sub(r"\s+", " ", line).strip()
        for line in text.splitlines()
        if line.strip()
    ]

    label_patterns = [
        r"name\s+of\s+(?:the\s+)?candidate",
        r"name\s+of\s+(?:the\s+)?student",
        r"candidate\s+name",
        r"student\s+name",
    ]

    for index, line in enumerate(lines):
        for label in label_patterns:
            match = re.search(rf"\b{label}\b\s*[:\-]?\s*(.*)$", line, re.IGNORECASE)
            if not match:
                continue
            value = match.group(1).strip()
            if not value and index + 1 < len(lines):
                value = lines[index + 1]
            cleaned = clean_ocr_value(value)
            if cleaned:
                return cleaned

    for index, line in enumerate(lines):
        if re.search(r"this\s+is\s+to\s+certify\s+that", line, re.IGNORECASE):
            remainder = re.sub(
                r".*?this\s+is\s+to\s+certify\s+that", "", line, flags=re.IGNORECASE
            ).strip(" :-")

            candidates = []
            if remainder:
                candidates.append(remainder)
            if index + 1 < len(lines):
                candidates.append(lines[index + 1])

            for candidate in candidates:
                cleaned = clean_ocr_value(candidate)
                if cleaned and not re.search(
                    r"\b(?:has successfully|register|number|completed|fulfilled|requirements)\b",
                    cleaned,
                    re.IGNORECASE,
                ):
                    return cleaned

    for line in lines:
        match = re.search(r"\bcandidate\b\s*[:\-]?\s*(.+)$", line, re.IGNORECASE)
        if match:
            cleaned = clean_ocr_value(match.group(1))
            if cleaned:
                return cleaned

    return None


def extract_register_number(text: str):
    patterns = [
        r"(?:register\s*(?:no|number)|reg\s*(?:no|number))"
        r"\s*[:#\-]?\s*([A-Za-z0-9][A-Za-z0-9/\-]{2,})",
        r"(?:roll\s*(?:no|number))"
        r"\s*[:#\-]?\s*([A-Za-z0-9][A-Za-z0-9/\-]{2,})",
        r"(?:enrolment|enrollment)\s*(?:no|number)"
        r"\s*[:#\-]?\s*([A-Za-z0-9][A-Za-z0-9/\-]{2,})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = re.sub(r"[^A-Za-z0-9]", "", match.group(1))
            return value.upper()
    return None
