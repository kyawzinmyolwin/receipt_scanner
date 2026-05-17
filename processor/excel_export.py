from __future__ import annotations

from pathlib import Path

import pandas as pd


def save_lines_to_excel(lines: list[str], output_path: Path) -> None:
    """Save extracted lines into a single-column Excel file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(lines, columns=["Extracted Text"])
    df.to_excel(output_path, index=False)
