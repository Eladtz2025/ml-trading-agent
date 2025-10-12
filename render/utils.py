"""Plotting helpers used in the dashboard applications."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


def _normalise_columns(df: pd.DataFrame) -> pd.DataFrame:
    lower = {col.lower(): col for col in df.columns}
    required = {"open", "high", "low", "close"}
    missing = required - set(lower)
    if missing:
        raise KeyError(f"DataFrame is missing required OHLC columns: {sorted(missing)}")
    return df.rename(columns={lower[name]: name for name in required})


def plot_ohlc(df: pd.DataFrame) -> go.Figure:
    normalised = _normalise_columns(df)
    fig = go.Figure(
        data=go.Candlestick(
            x=normalised.index,
            open=normalised["open"],
            high=normalised["high"],
            low=normalised["low"],
            close=normalised["close"],
        )
    )
    fig.update_layout(title="OHLC Data")
    return fig


def plot_predictions(df: pd.DataFrame, preds) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=preds, name="Predicted"))
    fig.update_layout(title="Model Predictions")
    return fig
