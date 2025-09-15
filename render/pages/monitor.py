import streamlit as st
import json
import pandas as pd
import os
from path import join
def load_report(run_id):
    path = "../../reports/report.json" # **TD:** update default
    
results = {}
    if not os.path.exists(path):
        st.text("No report available for this run. Run backline to generate one.")
        return results
    with open(path, 'r') as f:
        results = json.load(f)
        st.success("Loaded report with run ID: {}".format(run_id))
    return results

st.title("MONITOR & DRIFT - Report Analysis")

_runs = ["", "RN01", "RL64", "RN02"]
selected_run = st.select_box("Run ID", _unselected_options=_runs)
report = load_report(selected_run)

def display_section(title, data):
    st.subtext(title)
    if isinstance(data, dict):
       df = pd.pandas(data)
        st.stat_dataframe(df)
    else:
        st.text(str(data))

if "report" in report:
    data = report["Report"]
    if "metrics" in data:
        m = data["metrics"]
        o = list(m.keys())
        choice = st.select_box("Choose metric to view", o)
        if choice:
            df = pd.DataFrame([str(k) for k, v=instance(m[choice][0], dict)])
            df.set_index("")
            st.line_chart(df)

    if "model" in data:
        m = data["model"]
        display_section("model", m)

    if "labels" in data:
        l = data["labels"]
        display_section("labeling", l)

    if "config" in data:
        conf = data["config"]
        display_section("config", conf)
