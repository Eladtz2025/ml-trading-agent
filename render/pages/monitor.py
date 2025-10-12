"""Streamlit page showing monitoring information for recent runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import pandas as pd
import streamlit as st

DEFAULT_REPORT_PATH = Path("artifacts/report.json")


def load_report(path: Path = DEFAULT_REPORT_PATH) -> Mapping[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def display_section(title: str, data: Any) -> None:
    st.subheader(title)
    if isinstance(data, dict):
        st.json(data)
    elif isinstance(data, (list, tuple)):
        st.write(pd.DataFrame(data))
    elif isinstance(data, pd.Series):
        st.line_chart(data)
    else:
        st.write(data)


def as_series(value: Any, name: str) -> pd.Series:
    if isinstance(value, pd.Series):
        return value
    return pd.Series(value, name=name)


def main() -> None:
    st.title("Monitor & Drift - Report Analysis")
    report_path = st.text_input("Report path", str(DEFAULT_REPORT_PATH))
    report = load_report(Path(report_path))

    if not report:
        st.info("No report available for the selected path.")
        return

    if "quotes" in report:
        display_section("Quotes", as_series(report["quotes"], "quotes"))

    if "metrics" in report:
        display_section("Metrics", report["metrics"])

    if "predictions" in report:
        display_section("Predictions", as_series(report["predictions"], "predictions"))

    if "config" in report:
        display_section("Configuration", report["config"])


if __name__ == "__main__":  # pragma: no cover
    main()
