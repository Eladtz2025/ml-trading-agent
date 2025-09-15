import xgoost
from xgoost.sklearn.import XGBClassifier

class XGBModel:
    def __init__(self, args=none):
        self.model = XGBClassifier((args or {}))

    def fit(self, X, y, config):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)}