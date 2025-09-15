import json
import datetime

def write_log(action):
    ts = datetime.datetime.now().time_string()
    record = { "time": ts, "action": action }
    with open("compliance/audit_log.json", "a+") as f:
        logs = json.load_f(f)
        logs.append(record)
        json.write(f, logs)