import numpy as np
from sklearn.linear_model import LogisticRegression

class LogisticClassifier:
    """Logistic regression classifier with probability output."""
    
    def __init__(self):
        self.model = None
        
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'LogisticClassifier':
        self.model = LogisticRegression(max_iter=1000, random_state=42)
        self.model.fit(X, y)
        return self
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)
        
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)
    
    def score_single(self, x_scaled: np.ndarray, feature_names: list[str]) -> dict:
        x_2d = x_scaled.reshape(1, -1)
        prediction = int(self.model.predict(x_2d)[0])
        probabilities = self.model.predict_proba(x_2d)[0]
        
        return {
            'model': 'logistic_regression',
            'verdict': 'FRAUD' if prediction == 1 else 'LEGITIMATE',
            'probability_legit': float(probabilities[0]),
            'probability_fraud': float(probabilities[1]),
            'confidence': float(max(probabilities)),
            'weight_vector': {feature_names[i]: float(self.model.coef_[0][i]) for i in range(len(feature_names))},
            'intercept': float(self.model.intercept_[0])
        }
