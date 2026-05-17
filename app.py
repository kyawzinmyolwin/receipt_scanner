from __future__ import annotations

import argparse
from pathlib import Path

from processor.excel_export import save_lines_to_excel
from processor.ocr import extract_text
from processor.parser import split_text_lines


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract text from a receipt image and export it to Excel."
    )
    parser.add_argument("image", type=Path, help="Path to the input receipt image")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/output.xlsx"),
        help="Path to the output Excel file (default: outputs/output.xlsx)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    text = extract_text(args.image)
    lines = split_text_lines(text)
    save_lines_to_excel(lines, args.output)

    print(f"Done! Wrote {len(lines)} row(s) to {args.output}")


if __name__ == "__main__":
    main()
