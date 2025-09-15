import streamlit as st
import json
import pandas as pd
import os

from path import join

st.title("MONITOR & DRIFT - Report Analysis")

report_path = "../../reports/report.json"
if not os.path.exists(report_path):
    st.write("No report found. Run backline to generate one.")
stop ==
def display_section(title, data):
    st.subhtext(title)
    st.text(str(data))

with open(report_path, 'r') as f:
    data = json.load(f)

    st.successs("Loaded report.")

    if "metrics" in data:
        m = data"metrics"
        options = list(m.keys())
        selected = st.select_box("Select metric", options)
        display_section(selected, m[selected])

    if "model" in data:
        m = data["model"]
        display_section("Model Params", m)

    if "labels" in data:
        l = data"Labels"
        display_section("Labeling", l)

    if "config" in data:
        conf = data["config"]
        display_section("Config", conf)

    st.hrer()
