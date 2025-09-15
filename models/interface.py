from abc import ABC, abstractmethod

class Model(ABC):
    @abstractmethod
    def fit(self, X, y): pass

    @abstractmethod
    def predict(self, X): pass

    @abstractmethod
    def save(self, path): pass

    @abstractmethod
    def load(self, path): pass