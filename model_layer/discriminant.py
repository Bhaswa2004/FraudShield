import numpy as np

class DiscriminantClassifier:
    """Least-squares classification model."""
    
    def __init__(self):
        self.weights = None
        self.bias = None
        self.threshold = 0.5
        self._training_score_range = 1.0
        
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'DiscriminantClassifier':
        # Add bias column of 1s
        X_aug = np.column_stack([X, np.ones(X.shape[0])])
        w_aug = np.linalg.pinv(X_aug.T @ X_aug) @ X_aug.T @ y
        self.weights = w_aug[:-1]
        self.bias = w_aug[-1]
        
        scores = self.decision_function(X)
        self._training_score_range = max(np.max(np.abs(scores)), 1e-6)
        return self
        
    def decision_function(self, X: np.ndarray) -> np.ndarray:
        return X @ self.weights + self.bias
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        return (self.decision_function(X) >= self.threshold).astype(int)
        
    def score_single(self, x_scaled: np.ndarray, feature_names: list[str]) -> dict:
        raw_score = float(self.decision_function(x_scaled))
        return {
            'model': 'discriminant_function',
            'raw_score': raw_score,
            'threshold': float(self.threshold),
            'verdict': 'FRAUD' if raw_score >= self.threshold else 'LEGITIMATE',
            'confidence': min(abs(raw_score - self.threshold) / self._training_score_range, 1.0),
            'weighted_terms': {
                feature_name: {
                    'weight': float(w_i),
                    'scaled_value': float(x_i),
                    'contribution': float(w_i * x_i)
                } for feature_name, w_i, x_i in zip(feature_names, self.weights, x_scaled)
            },
            'bias': float(self.bias),
            'formula': 'g(x) = w₁x₁ + w₂x₂ + ... + w₆x₆ + b'
        }
