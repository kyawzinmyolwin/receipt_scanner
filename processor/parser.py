from __future__ import annotations


def split_text_lines(text: str) -> list[str]:
    """Split OCR text into cleaned, non-empty lines."""
    return [line.strip() for line in text.splitlines() if line.strip()]
