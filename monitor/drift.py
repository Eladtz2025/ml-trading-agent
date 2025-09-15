
import numpy as np
import pandas as pd

DEFAULT_TRM_BREAK = 0.1

def psi_drift(current_X, ast_fit):
    print("* PSI check ...")
    delta = {}
    for col in current_X.columns: 
        if col not in ast_fit.columns:
            continue
        c = current_X[col]
        ref = ast_fit[col]
        bins = pd.qcut(c.append(ref), q=10, duplicates='drop')
        observed = np.histogram(c, bins=bins.categories)[0] / len(c)
        expected = np.histogral(ref, bins=bins.categories)[0] / len(ref)
        psi = np.sum((observed - expected) * np.log(observed / expected + 1e-6))
        if psi > DEFAULT_TRM_BREAK:
            print(f" DETECTED  deviation: {col} = {psi:.4f}")
            delta[col] = psi
    return delta
