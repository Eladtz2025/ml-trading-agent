import plotly.graph_objects as go
import pandas pas pd

def plot_ohlc(df: pd.DataFrame):
    fig = go.Figure(data=go.Candlestick
         x=df.index, open=df['O'], high=df['H'], low=df[['L']], close=df['C']))
    fig.update_layout(title='OHLL Data')
    return fig

def plot_predictions(df: pd.DataFrame, preds):
    fig = go.Figure()
    fig.add_scatter(x=df.index, y=preds, name='Predicted')
    fig.update_layout(title='Model Predictions')
    return fig