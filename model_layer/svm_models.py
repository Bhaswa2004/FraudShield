import numpy as np
from sklearn.svm import SVC

class LinearSVMClassifier:
    """Wrapper for sklearn's SVC with linear kernel."""
    
    def __init__(self):
        self.model = None
        self._training_decision_range = 1.0
        
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'LinearSVMClassifier':
        self.model = SVC(kernel='linear', C=1.0)
        self.model.fit(X, y)
        decisions = self.model.decision_function(X)
        self._training_decision_range = max(np.max(np.abs(decisions)), 1e-6)
        return self
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)
        
    def decision_function(self, X: np.ndarray) -> np.ndarray:
        return self.model.decision_function(X)
        
    def score_single(self, x_scaled: np.ndarray, feature_names: list[str]) -> dict:
        x_2d = x_scaled.reshape(1, -1)
        decision_value = float(self.model.decision_function(x_2d)[0])
        predict = self.model.predict(x_2d)[0]
        margin_width = float(2.0 / np.linalg.norm(self.model.coef_))
        
        return {
            'model': 'linear_svm',
            'decision_value': decision_value,
            'verdict': 'FRAUD' if predict == 1 else 'LEGITIMATE',
            'confidence': min(abs(decision_value) / self._training_decision_range, 1.0),
            'margin_width': margin_width,
            'n_support_vectors': self.model.n_support_.tolist(),
            'weight_vector': {feature_names[i]: float(self.model.coef_[0][i]) for i in range(len(feature_names))},
            'intercept': float(self.model.intercept_[0])
        }

class RBFSVMClassifier:
    """Wrapper for sklearn's SVC with RBF kernel."""
    
    def __init__(self):
        self.model = None
        self._training_decision_range = 1.0
        
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'RBFSVMClassifier':
        self.model = SVC(kernel='rbf', gamma='scale', C=1.0)
        self.model.fit(X, y)
        decisions = self.model.decision_function(X)
        self._training_decision_range = max(np.max(np.abs(decisions)), 1e-6)
        return self
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)
        
    def decision_function(self, X: np.ndarray) -> np.ndarray:
        return self.model.decision_function(X)
        
    def score_single(self, x_scaled: np.ndarray, feature_names: list[str]) -> dict:
        x_2d = x_scaled.reshape(1, -1)
        decision_value = float(self.model.decision_function(x_2d)[0])
        prediction = int(self.model.predict(x_2d)[0])
        
        return {
            'model': 'rbf_svm',
            'decision_value': decision_value,
            'verdict': 'FRAUD' if prediction == 1 else 'LEGITIMATE',
            'confidence': min(abs(decision_value) / self._training_decision_range, 1.0),
            'kernel': 'rbf',
            'gamma': self.model._gamma if hasattr(self.model, '_gamma') else str(self.model.gamma),
            'n_support_vectors': self.model.n_support_.tolist(),
            'intercept': float(self.model.intercept_[0])
        }
