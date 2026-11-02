import textwrap
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageOps
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def add_image_to_pdf(pdf, image_path: Path):
    page_width, page_height = A4

    with Image.open(image_path) as original:
        image = ImageOps.exif_transpose(original).convert("RGB")
        image_width, image_height = image.size

        max_width = page_width - 40
        max_height = page_height - 70
        scale = min(max_width / image_width, max_height / image_height)

        width = image_width * scale
        height = image_height * scale
        x = (page_width - width) / 2
        y = (page_height - height) / 2

        pdf.drawImage(
            ImageReader(image), x, y,
            width=width, height=height,
            preserveAspectRatio=True, mask="auto",
        )

    pdf.showPage()


def draw_wrapped_text(pdf, value: str, x: int, y: int, width: int = 90, line_height: int = 15):
    lines = textwrap.wrap(str(value), width=width, break_long_words=True) or [""]

    for line in lines:
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = A4[1] - 50
        pdf.drawString(x, y, line)
        y -= line_height

    return y


def add_status_page(pdf, result):
    page_width, page_height = A4

    pdf.setTitle("Document Verification Report")

    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawCentredString(page_width / 2, page_height - 50, "DOCUMENT VERIFICATION REPORT")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(45, page_height - 78, "Generated: " + datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

    y = page_height - 115

    pdf.setFont("Helvetica-Bold", 13)
    y = draw_wrapped_text(pdf, "STATUS: " + result["status_label"], 45, y, width=75, line_height=18)

    y -= 12
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(45, y, "Extracted Candidate Details")
    y -= 22

    pdf.setFont("Helvetica", 10)
    fields = [
        ("Degree certificate candidate name", result["degree_name"]),
        ("Marksheet candidate name", result["marksheet_name"]),
        ("Degree certificate register number", result["degree_register"]),
        ("Marksheet register number", result["marksheet_register"]),
    ]
    for label, value in fields:
        y = draw_wrapped_text(pdf, f"{label}: {value or 'Not detected'}", 45, y)

    y -= 10
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(45, y, "Verification Findings")
    y -= 22

    pdf.setFont("Helvetica", 10)
    for index, finding in enumerate(result["findings"], start=1):
        y = draw_wrapped_text(pdf, f"{index}. {finding}", 45, y)
        y -= 6

    y -= 10
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(45, y, "Summary")
    y -= 20

    pdf.setFont("Helvetica", 10)
    y = draw_wrapped_text(pdf, result["reason"], 45, y)

    y -= 12
    pdf.setFont("Helvetica-Bold", 10)
    draw_wrapped_text(
        pdf,
        "Important: Matching fields do not prove that a document is genuine. "
        "This report performs an OCR-based comparison only.",
        45, y, width=85,
    )

    pdf.showPage()


def build_report_pdf(pdf_path: Path, degree_path: Path, marksheet_path: Path, result: dict):
    """Create the full report PDF: degree image, marksheet image, status page."""
    pdf = canvas.Canvas(str(pdf_path), pagesize=A4)
    add_image_to_pdf(pdf, degree_path)
    add_image_to_pdf(pdf, marksheet_path)
    add_status_page(pdf, result)
    pdf.save()
