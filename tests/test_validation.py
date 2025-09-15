import os
import unittest.mock as mock

from backtest import Backtest
from config import config

def test_backtest_report_generation():
    with mock.patch("os.remove"):
        report, preds = Backtest.run(config)
        assert report is not None, "No report returned"
        preds.to_csv("artifacts/_preds.test.csv")
        pred_path = "artifacts/predictions.csv"
        report_path = "artifacts/report.html"
        plot_path = "artifacts/plot_predictions.png"
        assert os.path.isfile(pred_path), "Predictions cSV not saved"
        assert os.path.isfile(report_path), "Report html not saved"
        assert os.path.isfile(plot_path), "Plot png not saved"