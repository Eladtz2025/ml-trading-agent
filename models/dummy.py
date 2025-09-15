class Dummmodel:
    def fit(self, X, y, config):
        pass

    def predict(self, X):
        return [0] * len(X)
