from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

import pandas as pd

# Extend this mapping to support more category keyword matches.
CATEGORY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Food": (
        "bread",
        "cake",
        "noodles",
        "grocery",
        "groceries",
        "fruit",
        "vegetable",
        "supermarket",
        "restaurant",
        "cafe",
        "coffee",
        "milk",
        "rice",
    ),
    "Transport": (
        "petrol",
        "fuel",
        "bus",
        "train",
        "taxi",
        "uber",
        "diesel",
        "parking",
        "toll",
    ),
}

MONEY_MANAGER_COLUMNS = [
    "Period",
    "Accounts",
    "Category",
    "Subcategory",
    "Note",
    "NZD",
    "Income/Expense",
    "Description",
    "Amount",
    "Currency",
    "Accounts",
]

DATE_PATTERNS = [
    re.compile(r"\b(\d{4})[-/](\d{1,2})[-/](\d{1,2})\b"),
    re.compile(r"\b(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})\b"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert outputs/*.xlsx receipt files into Money Manager TSV format."
    )
    parser.add_argument(
        "--inputs-dir",
        type=Path,
        default=Path("outputs"),
        help="Directory containing source XLSX files (default: outputs)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/money_manager.tsv"),
        help="Output TSV file path (default: outputs/money_manager.tsv)",
    )
    return parser.parse_args()


def detect_category(text: str) -> str:
    lowered = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return category
    return "Other"


def detect_date(lines: list[str], fallback_file: Path) -> str:
    for line in lines:
        for pattern in DATE_PATTERNS:
            match = pattern.search(line)
            if not match:
                continue

            groups = match.groups()
            try:
                if len(groups[0]) == 4:
                    dt = datetime(int(groups[0]), int(groups[1]), int(groups[2]))
                else:
                    year = int(groups[2])
                    if year < 100:
                        year += 2000
                    dt = datetime(year, int(groups[1]), int(groups[0]))
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue

    return datetime.fromtimestamp(fallback_file.stat().st_mtime).strftime("%Y-%m-%d")


def detect_amount(lines: list[str]) -> float:
    amount_regex = re.compile(r"(?<!\d)(\d{1,5}(?:[.,]\d{3})*(?:[.,]\d{2})?)(?!\d)")
    candidates: list[float] = []
    for line in lines:
        line_lower = line.lower()
        matches = amount_regex.findall(line)
        parsed: list[float] = []
        for m in matches:
            normalized = m.replace(",", "")
            try:
                parsed.append(float(normalized))
            except ValueError:
                continue
        if not parsed:
            continue

        # Prioritize likely total lines.
        if any(tag in line_lower for tag in ("total", "amount due", "balance")):
            return max(parsed)
        candidates.extend(parsed)

    return max(candidates) if candidates else 0.0


def load_lines(xlsx_path: Path) -> list[str]:
    df = pd.read_excel(xlsx_path)
    if "Extracted Text" in df.columns:
        values = df["Extracted Text"].dropna().astype(str).tolist()
    else:
        values = df.astype(str).fillna("").agg(" ".join, axis=1).tolist()
    return [v.strip() for v in values if v.strip()]


def build_row(xlsx_path: Path) -> dict[str, str | float]:
    lines = load_lines(xlsx_path)
    full_text = " ".join(lines)

    period = detect_date(lines, xlsx_path)
    category = detect_category(full_text)
    amount = detect_amount(lines)

    row = {
        "Period": period,
        "Accounts": "ASB",
        "Category": category,
        "Subcategory": "",
        "Note": "",
        "NZD": amount,
        "Income/Expense": "Exp.",
        "Description": "",
        "Amount": amount,
        "Currency": "NZD",
    }
    return row


def main() -> None:
    args = parse_args()

    xlsx_files = sorted(
        p for p in args.inputs_dir.glob("*.xlsx") if p.name != args.output.name
    )
    if not xlsx_files:
        raise FileNotFoundError(f"No .xlsx files found in {args.inputs_dir}")

    rows = [build_row(p) for p in xlsx_files]
    out_df = pd.DataFrame(rows)
    out_df = out_df.reindex(columns=MONEY_MANAGER_COLUMNS)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(args.output, sep="\t", index=False)

    print(f"Wrote {len(out_df)} row(s) to {args.output}")


if __name__ == "__main__":
    main()
