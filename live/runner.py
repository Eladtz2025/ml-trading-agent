import time
import subprocess

CONFIG = "packs/example_aplz/config.yaml"

while True:
    print("[LIVE] ", time.ctime(), " running...")
    subprocess.run("python main.py --config " + CONFIG)
    time.sleep(60)