import numpy as np

def generate_dataset(n_samples=500, seed=42) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """
    Generate a synthetic fraud dataset.
    Returns (X, y, feature_names).
    """
    feature_names = ['amount', 'hour', 'merchant_risk', 'distance_from_home', 'transaction_velocity', 'is_international']
    rng = np.random.RandomState(seed)
    
    n_fraud = int(n_samples * 0.2)
    n_legit = n_samples - n_fraud
    
    # Legitimate
    l_amount = np.clip(rng.exponential(50, n_legit) + 10, 10, 500)
    l_hour = np.clip(rng.normal(14, 4, n_legit), 0, 23)
    l_merchant_risk = rng.beta(2, 8, n_legit)
    l_distance = np.clip(rng.exponential(10, n_legit), 0, 100)
    l_velocity = np.clip(rng.poisson(1, n_legit) + 1, 1, 10)
    l_intl = rng.binomial(1, 0.1, n_legit)
    
    # Fraudulent
    f_amount = np.clip(rng.exponential(200, n_fraud) + 100, 100, 10000)
    f_hour = np.clip(rng.choice([0,1,2,3,4,5,22,23], n_fraud) + rng.normal(0, 0.5, n_fraud), 0, 23)
    f_merchant_risk = rng.beta(7, 3, n_fraud)
    f_distance = np.clip(rng.exponential(50, n_fraud) + 20, 0, 500)
    f_velocity = np.clip(rng.poisson(4, n_fraud) + 2, 1, 20)
    f_intl = rng.binomial(1, 0.6, n_fraud)
    
    X_legit = np.column_stack([l_amount, l_hour, l_merchant_risk, l_distance, l_velocity, l_intl])
    X_fraud = np.column_stack([f_amount, f_hour, f_merchant_risk, f_distance, f_velocity, f_intl])
    
    X = np.vstack([X_legit, X_fraud])
    y = np.hstack([np.zeros(n_legit), np.ones(n_fraud)])
    
    # Shuffle
    idx = rng.permutation(n_samples)
    X = X[idx]
    y = y[idx]
    
    return X, y, feature_names
