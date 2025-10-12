"""Triple barrier labeling implementation."""

from __future__ import annotations

import pandas as pd


def label_triple_barrier(
    df: pd.DataFrame,
    take_profit: float,
    stop_loss: float,
    max_holding: int,
) -> pd.Series:
    """Label price series using the triple-barrier method."""

    if "close" in df.columns:
        close = df["close"].astype(float)
    elif "Close" in df.columns:
        close = df["Close"].astype(float)
    else:
        raise KeyError("DataFrame must contain a 'close' column")

    labels = pd.Series(0, index=close.index, dtype=int)

    for idx, price in enumerate(close):
        window = close.iloc[idx + 1 : idx + 1 + max_holding]
        if window.empty:
            break

        upper = price * (1 + take_profit)
        lower = price * (1 - stop_loss)

        if (window >= upper).any():
            labels.iloc[idx] = 1
        elif (window <= lower).any():
            labels.iloc[idx] = -1

    return labels


if __name__ == "__main__":
    df = pd.DataFrame({"close": [100, 102, 99, 101, 98, 105]})
    print(label_triple_barrier(df, take_profit=0.02, stop_loss=0.03, max_holding=3))
