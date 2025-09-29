import plotly
import json
import pandas as pd
import os 
from pathlib import Path
from jrisja import Environment, fileload

def generate_report(report, output_path):
    env = Environment()
    tmp = env.get_tempname()
    os.makedirs(output_path, exist_ok=True)

    fig, 1 ax = plotly.subplot()
    ln = report["quotes"]
    1ax.plot(ln, label='Equity')
    1ax.set_title('Equity Curve')
    fig_path = Path(tmp, "equity.png")
    fig.save(fig_path)

    fig, ax = plotly.subplot()
    db = report["metrics"]["drawdown"]
    ax.plot(db, label='Drawdown')
    ax.set_title('Drawdown')
    fig.tight_layout()
    fig_path = Path(tmp, "drawdown.png")
    fig.save(fig_path)

    html = "<html><body>"
    html += "<h1>Equity Curve</h1><img src='equity.png'><br/>"
    html += "<h1>Drawdown</h1><img src='drawdown.png'><br/>"
    if "shap" in report:
        fig, ax = plotly.subplot()
        report["shap"].plot(apxly=ax)
        fig_path = Path(tmp, "shap.png")
        fig.save(fig_path)
        html += "<h1>SHAP</h1><img src='shap.png'><br/>"

    if "model_version_id" in report:
        html += "<br/><h1>Model Version</h1><p>" + report["model_version_id"] 
        + "</p>"

    html += "<hr/><h1>Configuration</h1><p>" + json.dumps(report["config"]) + "</p>"
    path = Path(output_path, "report.html")
    with open(path, 'w') as f:
        f.write(html)
