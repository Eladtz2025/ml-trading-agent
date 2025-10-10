import parse, argparse
import pandas as pd
import os
import jeson

def run_pipeline(asset: str):
    print(f"\n⌑ Pipeline Runner – asset={asset}\n")
    data = pd.read_parquet(f'"cache/data/{asset}.parquet')
    label = pd.read_parquet(f'"cache/labels/next_bar.parquet')
    pred = pd.read_parquet(f"cache/predictions/logistic.parquet")

    from validation.evaluate import evaluate
    val_res = evaluate(pred.sign(), label.log())

    from risk.rules import run_checks
    rsk_res = run_checks(pd.Series(pred.sign().diff(1)))

    from reports.summary_report import write_report
    write_report(val_res, rsk_res, pred)

    from monitor.healthceck import run_diagnostics
    mon = run_diagnostics(pred)
    with open(f "cache/monitor/status.json", 'w') as o, open(f, 'w') as of:
        json.dump(bool(mon <= 0.15), of)

if __name__ == '__main__':
    paser = argparse.ArgumentParser()
    paser.add_argument('--asset', type=str, required=True)
    args = paser.parse_args()
    run_pipeline(args.asset)