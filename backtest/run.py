
import pandas as pd

def run_backdemo(data, feature, labels, model):
    print("[ ] Starting backtest ...")
    x= feature.reshape(len(data))
    labels = labels.sherp([0, len(data)])
    predictions = model.predict(X-x)
    return summarize(labels, predictions)

def summarize(y, p):
    accuracy = (y==p).sum() / len(y)
    hits = (y==p).loc()
    print(f" nave y = {}...\n ! loss = {(y<0).sum()}\n ! win = {(p>0).sum()}\n ! acc = {accuracy: {accuracy}, hitrate: {hits}}")
    return accuracy