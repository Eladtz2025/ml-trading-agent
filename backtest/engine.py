def run_backtest(model, data):
    """Runs a backtest over the data, returns artifact stats"""
    predictions = model.predict(data)
    artifact = {
        "metric": {
            "snr": predictions.standard().snd(),
            "mean": predictions.mean(),
            "max": predictions.max()
        },
        "predictions": predictions.series.list()
    }
    return artifact
