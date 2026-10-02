import numpy as np
from sklearn.model_selection import train_test_split
from data_layer.sample_data import generate_dataset
from data_layer.feature_engineering import FeatureScaler
from model_layer.discriminant import DiscriminantClassifier
from model_layer.svm_models import LinearSVMClassifier, RBFSVMClassifier
from model_layer.logistic_model import LogisticClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, accuracy_score

class ModelManager:
    """Manages training and prediction for fraud detection models."""
    
    def __init__(self):
        self._initialize()
        
    def _initialize(self):
        X, y, feature_names = generate_dataset()
        self.feature_names = feature_names
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        self.scaler = FeatureScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.discriminant = DiscriminantClassifier()
        self.discriminant.fit(X_train_scaled, y_train)
        
        self.svm = LinearSVMClassifier()
        self.svm.fit(X_train_scaled, y_train)
        
        self.rbf_svm = RBFSVMClassifier()
        self.rbf_svm.fit(X_train_scaled, y_train)
        
        self.logistic = LogisticClassifier()
        self.logistic.fit(X_train_scaled, y_train)
        
        # Generate synthetic 2D dataset for kernel boundary visualization
        self._generate_2d_boundary_data()
        
        self.X_test_scaled = X_test_scaled
        self.y_test = y_test
        
        print(f'Models trained. Train: {len(X_train)}, Test: {len(X_test)}')
        
    def predict(self, features_dict: dict) -> dict:
        x = np.array([features_dict[name] for name in self.feature_names])
        x_scaled = self.scaler.transform_single(x)
        
        disc_result = self.discriminant.score_single(x_scaled, self.feature_names)
        svm_result = self.svm.score_single(x_scaled, self.feature_names)
        rbf_result = self.rbf_svm.score_single(x_scaled, self.feature_names)
        logistic_result = self.logistic.score_single(x_scaled, self.feature_names)
        
        return {
            'discriminant': disc_result,
            'svm': svm_result,
            'rbf_svm': rbf_result,
            'logistic': logistic_result,
            'features': features_dict,
            'is_fraud_predicted': (disc_result['verdict'] == 'FRAUD') or (svm_result['verdict'] == 'FRAUD')
        }

    def _generate_2d_boundary_data(self):
        """Generate a synthetic 2D dataset for kernel boundary visualization.
        Uses concentric rings pattern - fraud in center, legit in outer ring.
        This pattern is NOT linearly separable, demonstrating why RBF kernel is needed.
        """
        rng = np.random.RandomState(42)
        n_samples = 200
        
        # Inner cluster (fraud) - small radius
        n_fraud = n_samples // 3
        r_fraud = rng.uniform(0, 1.5, n_fraud)
        theta_fraud = rng.uniform(0, 2 * np.pi, n_fraud)
        x1_fraud = r_fraud * np.cos(theta_fraud)
        x2_fraud = r_fraud * np.sin(theta_fraud)
        
        # Outer ring (legit) - large radius  
        n_legit = n_samples - n_fraud
        r_legit = rng.uniform(2.5, 4.0, n_legit)
        theta_legit = rng.uniform(0, 2 * np.pi, n_legit)
        x1_legit = r_legit * np.cos(theta_legit)
        x2_legit = r_legit * np.sin(theta_legit)
        
        # Add some noise
        noise = 0.3
        x1_fraud += rng.normal(0, noise, n_fraud)
        x2_fraud += rng.normal(0, noise, n_fraud)
        x1_legit += rng.normal(0, noise, n_legit)
        x2_legit += rng.normal(0, noise, n_legit)
        
        X_2d = np.vstack([
            np.column_stack([x1_fraud, x2_fraud]),
            np.column_stack([x1_legit, x2_legit])
        ])
        y_2d = np.hstack([np.ones(n_fraud), np.zeros(n_legit)])
        
        # Shuffle
        idx = rng.permutation(len(y_2d))
        X_2d = X_2d[idx]
        y_2d = y_2d[idx]
        
        # Train both SVMs on 2D data
        from sklearn.svm import SVC
        self._svm_2d_linear = SVC(kernel='linear', C=1.0)
        self._svm_2d_linear.fit(X_2d, y_2d)
        
        self._svm_2d_rbf = SVC(kernel='rbf', gamma='scale', C=1.0)
        self._svm_2d_rbf.fit(X_2d, y_2d)
        
        self._X_2d = X_2d
        self._y_2d = y_2d

    def get_boundary_data(self, kernel: str = 'linear') -> dict:
        """Return grid data for 2D decision boundary visualization."""
        model = self._svm_2d_linear if kernel == 'linear' else self._svm_2d_rbf
        
        # Create mesh grid
        x_min, x_max = self._X_2d[:, 0].min() - 1, self._X_2d[:, 0].max() + 1
        y_min, y_max = self._X_2d[:, 1].min() - 1, self._X_2d[:, 1].max() + 1
        
        resolution = 80
        xx = np.linspace(x_min, x_max, resolution)
        yy = np.linspace(y_min, y_max, resolution)
        XX, YY = np.meshgrid(xx, yy)
        grid_points = np.column_stack([XX.ravel(), YY.ravel()])
        
        Z = model.decision_function(grid_points).reshape(XX.shape)
        
        # Get support vectors
        sv = model.support_vectors_.tolist()
        
        return {
            'kernel': kernel,
            'grid': {
                'x_min': float(x_min), 'x_max': float(x_max),
                'y_min': float(y_min), 'y_max': float(y_max),
                'resolution': resolution,
                'z_values': Z.tolist()  # 2D array of decision function values
            },
            'points': {
                'X': self._X_2d.tolist(),
                'y': self._y_2d.tolist()
            },
            'support_vectors': sv,
            'accuracy': float(accuracy_score(self._y_2d, model.predict(self._X_2d)))
        }

    def get_metrics(self) -> dict:
        """Compute classification metrics for all models on test data."""
        models = {
            'discriminant': self.discriminant,
            'linear_svm': self.svm,
            'rbf_svm': self.rbf_svm,
            'logistic': self.logistic
        }
        
        results = {}
        for name, model in models.items():
            y_pred = model.predict(self.X_test_scaled)
            cm = confusion_matrix(self.y_test, y_pred).tolist()
            results[name] = {
                'accuracy': float(accuracy_score(self.y_test, y_pred)),
                'precision': float(precision_score(self.y_test, y_pred, zero_division=0)),
                'recall': float(recall_score(self.y_test, y_pred, zero_division=0)),
                'f1': float(f1_score(self.y_test, y_pred, zero_division=0)),
                'confusion_matrix': cm  # [[TN, FP], [FN, TP]]
            }
        
        results['note'] = (
            'In fraud detection, false negatives (missed fraud) are far more costly than '
            'false positives (legitimate transactions flagged as fraud). A missed fraud '
            'results in direct financial loss, while a false positive merely causes '
            'temporary inconvenience. Therefore, recall (sensitivity) is often prioritized '
            'over precision in fraud detection systems.'
        )
        
        return results

    def get_feature_importance(self) -> dict:
        """Get feature importance from all models."""
        importance = {}
        
        # Discriminant function weights (absolute values as importance)
        disc_weights = np.abs(self.discriminant.weights)
        disc_importance = disc_weights / disc_weights.sum()
        importance['discriminant'] = {
            self.feature_names[i]: {
                'raw_weight': float(self.discriminant.weights[i]),
                'abs_weight': float(disc_weights[i]),
                'importance': float(disc_importance[i])
            } for i in range(len(self.feature_names))
        }
        
        # Linear SVM weights
        svm_weights = np.abs(self.svm.model.coef_[0])
        svm_importance = svm_weights / svm_weights.sum()
        importance['linear_svm'] = {
            self.feature_names[i]: {
                'raw_weight': float(self.svm.model.coef_[0][i]),
                'abs_weight': float(svm_weights[i]),
                'importance': float(svm_importance[i])
            } for i in range(len(self.feature_names))
        }
        
        # Logistic regression weights
        log_weights = np.abs(self.logistic.model.coef_[0])
        log_importance = log_weights / log_weights.sum()
        importance['logistic'] = {
            self.feature_names[i]: {
                'raw_weight': float(self.logistic.model.coef_[0][i]),
                'abs_weight': float(log_weights[i]),
                'importance': float(log_importance[i])
            } for i in range(len(self.feature_names))
        }
        
        # Aggregate importance (average across linear models)
        aggregate = {}
        for i, name in enumerate(self.feature_names):
            avg_imp = (disc_importance[i] + svm_importance[i] + log_importance[i]) / 3
            aggregate[name] = float(avg_imp)
        importance['aggregate'] = aggregate
        importance['ranked'] = sorted(aggregate.items(), key=lambda x: x[1], reverse=True)
        
        return importance
    
    def retrain_with_data(self, X_new: np.ndarray, y_new: np.ndarray) -> dict:
        """Retrain all models with new data. Returns before/after metrics comparison."""
        old_metrics = self.get_metrics()
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_new, y_new, test_size=0.2, random_state=42, stratify=y_new
        )
        
        self.scaler = FeatureScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.discriminant = DiscriminantClassifier()
        self.discriminant.fit(X_train_scaled, y_train)
        
        self.svm = LinearSVMClassifier()
        self.svm.fit(X_train_scaled, y_train)
        
        self.rbf_svm = RBFSVMClassifier()
        self.rbf_svm.fit(X_train_scaled, y_train)
        
        self.logistic = LogisticClassifier()
        self.logistic.fit(X_train_scaled, y_train)
        
        self.X_test_scaled = X_test_scaled
        self.y_test = y_test
        self._generate_2d_boundary_data()
        
        new_metrics = self.get_metrics()
        
        return {
            'status': 'success',
            'training_samples': len(X_train),
            'test_samples': len(X_test),
            'fraud_ratio': float(y_new.mean()),
            'before': {k: v for k, v in old_metrics.items() if k != 'note'},
            'after': {k: v for k, v in new_metrics.items() if k != 'note'}
        }
    
    def get_roi_analysis(self) -> dict:
        """Calculate ROI analysis based on transaction history."""
        from db.database import get_history
        
        transactions = get_history(limit=1000)
        total_txns = len(transactions)
        fraud_detected = sum(1 for t in transactions if t.get('is_fraud_predicted'))
        legit_txns = total_txns - fraud_detected
        
        total_amount = sum(float(t.get('amount', 0)) for t in transactions)
        fraud_amount = sum(float(t.get('amount', 0)) for t in transactions if t.get('is_fraud_predicted'))
        
        prevention_rate = 0.85
        avg_fraud_loss_multiplier = 3.0
        estimated_loss_prevented = fraud_amount * prevention_rate
        total_cost_prevented = estimated_loss_prevented * avg_fraud_loss_multiplier
        
        metrics = self.get_metrics()
        best_model = max(
            [(k, v) for k, v in metrics.items() if isinstance(v, dict)],
            key=lambda x: x[1].get('f1', 0)
        )
        
        return {
            'summary': {
                'total_transactions': total_txns,
                'fraud_detected': fraud_detected,
                'legitimate': legit_txns,
                'fraud_rate': float(fraud_detected / max(total_txns, 1) * 100),
                'total_amount': float(total_amount),
                'fraud_amount': float(fraud_amount),
                'legit_amount': float(total_amount - fraud_amount)
            },
            'roi': {
                'estimated_loss_prevented': float(estimated_loss_prevented),
                'total_cost_prevented': float(total_cost_prevented),
                'prevention_rate': prevention_rate,
                'fraud_loss_multiplier': avg_fraud_loss_multiplier,
                'false_positive_cost': 25.0
            },
            'best_model': {
                'name': best_model[0],
                'f1': best_model[1]['f1'],
                'precision': best_model[1]['precision'],
                'recall': best_model[1]['recall']
            },
            'assumptions': [
                'Total fraud cost is approximately 3x the transaction amount (chargebacks, investigation, reputation)',
                '85% of detected fraud transactions are successfully prevented',
                'Average false positive costs $25 in customer friction',
                'ROI improves with higher recall (fewer missed frauds)'
            ]
        }
