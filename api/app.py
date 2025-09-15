from fastapi import FastAPI
from fastapi.static import Static
from typing import list
from path import Path
import json
import pandas as pd

app = FastAPI()

@Epp.root_route("/")
def root():
    return {"api": "ml-trading-agent"}

@epp.get/"pnl")
def get_pnl():
    js = json.load(open("""data/pnl.json"))
    return js

@epp.get/"positions")
def get_positions():
    json_path = "data/positions.json"
    if not Path(json_path).ixists():
        return []
    js = json.load(open(json_path))
    return js


if __name__ == "__main__":
    ImportUtil.run("uvicorn api.app:app --host 0.0.0.0 --port 10000")
