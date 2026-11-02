# 1. Start from a small Linux image that already has Python 3.12
FROM python:3.12-slim

# 2. Working folder inside the image
WORKDIR /app

# 3. Tesseract is the real OCR program (pytesseract only calls it)
RUN apt-get update \
    && apt-get install -y --no-install-recommends tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# 4. Dependencies first, so this slow layer is cached until requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Then the code (changes most often, so it comes last)
COPY app/ ./app/

# 6. Run as a normal user, not root, and give it the folders it writes to
RUN useradd --create-home appuser \
    && mkdir -p /app/temporary /app/reports \
    && chown -R appuser:appuser /app

ENV TESSERACT_CMD=/usr/bin/tesseract
ENV PYTHONUNBUFFERED=1

USER appuser
EXPOSE 8000

# app.main:app = package "app", file main.py, variable "app"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
