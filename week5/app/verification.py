import re

from ocr import extract_candidate_name, extract_register_number


def normalize_name(value):
    if not value:
        return None
    return re.sub(r"[^a-z]", "", value.lower())


def normalize_register(value):
    if not value:
        return None
    return re.sub(r"[^A-Za-z0-9]", "", value).upper()


def documents_match(degree_text: str, marksheet_text: str):
    degree_name = extract_candidate_name(degree_text)
    marksheet_name = extract_candidate_name(marksheet_text)
    degree_register = extract_register_number(degree_text)
    marksheet_register = extract_register_number(marksheet_text)

    findings = []
    actual_mismatches = []
    missing_fields = []

    # ---- Candidate name checks ----
    if not degree_name:
        missing_fields.append("Degree certificate candidate name")
        findings.append("Candidate name could not be reliably detected in the degree certificate.")

    if not marksheet_name:
        missing_fields.append("Marksheet candidate name")
        findings.append("Candidate name could not be reliably detected in the marksheet.")

    if degree_name and marksheet_name:
        if normalize_name(degree_name) != normalize_name(marksheet_name):
            actual_mismatches.append("Candidate name")
            findings.append(
                f"Candidate names differ: degree certificate says '{degree_name}', "
                f"while marksheet says '{marksheet_name}'."
            )
        else:
            findings.append(f"Candidate name matches: '{degree_name}' and '{marksheet_name}'.")

    # ---- Register number checks ----
    if not degree_register:
        missing_fields.append("Degree certificate register number")
        findings.append("Register number could not be detected in the degree certificate.")

    if not marksheet_register:
        missing_fields.append("Marksheet register number")
        findings.append("Register number could not be detected in the marksheet.")

    if degree_register and marksheet_register:
        if normalize_register(degree_register) != normalize_register(marksheet_register):
            actual_mismatches.append("Register number")
            findings.append(
                f"Register numbers differ: degree certificate has '{degree_register}', "
                f"while marksheet has '{marksheet_register}'."
            )
        else:
            findings.append(f"Register number matches: '{degree_register}'.")

    # ---- Three distinct outcomes ----
    if actual_mismatches:
        status = "MISMATCH"
        status_label = "MISMATCH FOUND"
        reason = (
            "One or more extracted fields differ between the documents. "
            "Review the findings below."
        )
    elif missing_fields:
        status = "UNABLE_TO_VERIFY"
        status_label = "UNABLE TO VERIFY - INFORMATION MISSING"
        reason = (
            "One or more required fields could not be reliably extracted. "
            "This is not automatically a mismatch. Review the source images "
            "and OCR results."
        )
    else:
        status = "MATCH"
        status_label = "FIELDS MATCH"
        reason = (
            "The extracted candidate names and register numbers match "
            "across both documents. This comparison does not establish "
            "document authenticity."
        )

    return {
        "status": status,
        "status_label": status_label,
        "reason": reason,
        "degree_name": degree_name,
        "marksheet_name": marksheet_name,
        "degree_register": degree_register,
        "marksheet_register": marksheet_register,
        "findings": findings,
        "actual_mismatches": actual_mismatches,
        "missing_fields": missing_fields,
    }
