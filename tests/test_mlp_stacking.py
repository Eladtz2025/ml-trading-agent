import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from models.mlp_stacking import StackedModelCPU

def main():
    print("🧪 Running test for StackedModelCPU...")
    X, y = make_classification(n_samples=500, n_features=8, n_informative=6, random_state=42)
    model = StackedModelCPU()
    model.train_and_log(X, y)
    print("✅ Test completed successfully.")

if __name__ == "__main__":
    main()
