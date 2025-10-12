"""Generate Markdown summaries for validation, risk and trading results."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Mapping, Optional

import pandas as pd

from .metrics_table import build_metrics_table

DEFAULT_FILE = Path("cache/reports") / f"summary_{datetime.utcnow().date()}.md"


def write_report(
    val_res: Mapping[str, float],
    rsk_res: Mapping[str, float],
    trd_res: pd.Series,
    backtest_frame: Optional[pd.DataFrame] = None,
    path: Path = DEFAULT_FILE,
) -> Path:
    lines = ["## Summary Report", ""]

    lines.append("### Validation")
    for key, value in val_res.items():
        lines.append(f"- **{key}**: {value:.4f}")

    lines.append("")
    lines.append("### Risk")
    for key, value in rsk_res.items():
        lines.append(f"- **{key}**: {value:.4f}")

    lines.append("")
    lines.append("### Trading")
    for idx, value in trd_res.items():
        lines.append(f"- **{idx}**: {float(value):.4f}")

    if backtest_frame is not None and not backtest_frame.empty:
        metrics = build_metrics_table(backtest_frame)
        lines.append("")
        lines.append("### Performance Metrics")
        lines.append(metrics.to_markdown(index=False))

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


if __name__ == "__main__":  # pragma: no cover
    import json

    with open("cache/validation/logistic.json", "r", encoding="utf-8") as fh:
        val = json.load(fh)
    with open("cache/risk/logistic.json", "r", encoding="utf-8") as fh:
        rsk = json.load(fh)
    trd = pd.read_parquet("cache/backtest/baseline.parquet").iloc[:, 0]
    write_report(val, rsk, trd)
