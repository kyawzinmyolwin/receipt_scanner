from __future__ import annotations

from pathlib import Path

from PIL import Image
import pytesseract


def extract_text(image_path: Path) -> str:
    """Extract raw text from an image via Tesseract OCR."""
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    with Image.open(image_path) as img:
        return pytesseract.image_to_string(img)
