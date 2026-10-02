import numpy as np

class FeatureScaler:
    """Standardizes features by removing the mean and scaling to unit variance."""
    
    def __init__(self):
        self.mean_ = None
        self.std_ = None
        
    def fit(self, X: np.ndarray) -> 'FeatureScaler':
        self.mean_ = np.mean(X, axis=0)
        self.std_ = np.std(X, axis=0)
        self.std_[self.std_ == 0] = 1.0 # prevent division by zero
        return self
        
    def transform(self, X: np.ndarray) -> np.ndarray:
        return (X - self.mean_) / self.std_
        
    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.fit(X).transform(X)
        
    def transform_single(self, x: np.ndarray) -> np.ndarray:
        return (x - self.mean_) / self.std_
