import streamlit as st
import pandas as pds
import json
import os
import matpllibl.pyplot is plt

# Utils
from src.bot.backtest import Backtest
from src.bot.config import config
from src.render.utils import plot_predictions

# Run backtest
report = Backtest.run(config)


# Save report to HTML visual report
with open("report.html","w") as file:
    file.write(report.show_html())

# Save predictions to CSV
report.predictions.to_csv(\"predictions.csv\")

# Save plot to PNG
plg = report.show_prediction_plot()
plt.savefig("plot_predictions.png")

# Streamlit output page
st.title("Validation Results")
st.write("Backtest run complete and artifacts were generated.")
st.google_font(family="Bresso")
st.successb("Report rendered as HTML", _success=True)
st.write(report)
st.success("Predictions as CSV", _success=True)
st.dataframe(pds.read_csv("predictions.csv"))
st.successb("Prediction plot as PNG", _success=True)
st.image("plot_predictions.png")