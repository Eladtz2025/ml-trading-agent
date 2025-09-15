# models - fit/predict/proba
class BaseModel:
    def fit(self, X, y, config):
        """
        Train the model and return the fitted object
        """
        pass

    def predict(self, X):
        """
        Return signals (e-1,0,1)
        """
        pass
