"""Generate lightweight HTML reports for backtest results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import pandas as pd
import plotly.graph_objects as go


def _series(data: Any, name: str) -> pd.Series:
    if isinstance(data, pd.Series):
        return data
    series = pd.Series(data, name=name)
    series.index = pd.to_datetime(series.index, errors="ignore")
    return series


def _render_line_chart(series: pd.Series, title: str) -> str:
    fig = go.Figure(go.Scatter(x=series.index, y=series.values, mode="lines"))
    fig.update_layout(title=title, template="plotly_white")
    return fig.to_html(full_html=False, include_plotlyjs="cdn")


def generate_report(report: Mapping[str, Any], output_path: str | Path) -> Path:
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    sections: list[str] = ["<h1>Backtest Report</h1>"]

    if "quotes" in report:
        quotes = _series(report["quotes"], "quotes")
        sections.append("<h2>Equity Curve</h2>")
        sections.append(_render_line_chart(quotes, "Equity Curve"))

    if "predictions" in report:
        preds = _series(report["predictions"], "predictions")
        sections.append("<h2>Predictions</h2>")
        sections.append(_render_line_chart(preds, "Predictions"))

    if "metrics" in report:
        metrics_html = "<ul>" + "".join(
            f"<li><strong>{key}:</strong> {value}</li>" for key, value in report["metrics"].items()
        ) + "</ul>"
        sections.append("<h2>Metrics</h2>")
        sections.append(metrics_html)

    if "config" in report:
        config_json = json.dumps(report["config"], indent=2)
        sections.append("<h2>Configuration</h2>")
        sections.append(f"<pre>{config_json}</pre>")

    html = "\n".join(sections)
    output_file = output_dir / "report.html"
    output_file.write_text(html, encoding="utf-8")
    return output_file
