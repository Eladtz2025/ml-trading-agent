"""Streamlit page that surfaces validation artefacts."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

ARTIFACT_DIR = Path("reports")


def _load_predictions() -> pd.DataFrame | None:
    csv_path = ARTIFACT_DIR / "predictions.csv"
    if not csv_path.exists():
        return None
    return pd.read_csv(csv_path)


def _load_report_html() -> str | None:
    html_path = ARTIFACT_DIR / "latest.html"
    if not html_path.exists():
        return None
    return html_path.read_text(encoding="utf-8")


def render() -> None:
    """Render the validation artefacts within Streamlit."""

    st.title("Validation Results")
    st.write(
        "Review the latest backtest artefacts including prediction tables and "
        "plots."
    )

    html_report = _load_report_html()
    if html_report is not None:
        st.download_button(
            "Download validation report",
            data=html_report,
            file_name="validation_report.html",
            mime="text/html",
        )
    else:
        st.info("No HTML validation report found.")

    predictions = _load_predictions()
    if predictions is not None:
        st.subheader("Predictions")
        st.dataframe(predictions)
    else:
        st.info("Prediction CSV not available.")

    plot_path = ARTIFACT_DIR / "prediction_plot.png"
    if plot_path.exists():
        st.subheader("Prediction Plot")
        st.image(str(plot_path))
    else:
        st.info("Prediction plot not found.")


if __name__ == "__main__":
    render()
