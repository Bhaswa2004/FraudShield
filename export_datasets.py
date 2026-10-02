import os
import csv
import numpy as np
from data_layer.sample_data import generate_dataset

def export_csv_files():
    # 1. Export main 500-sample synthetic dataset
    X, y, feature_names = generate_dataset(n_samples=500, seed=42)
    
    dataset_path = os.path.join(os.getcwd(), 'fraudshield_dataset.csv')
    with open(dataset_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(feature_names + ['is_fraud'])
        for row, label in zip(X, y):
            writer.writerow([
                round(row[0], 2),  # amount
                round(row[1], 1),  # hour
                round(row[2], 4),  # merchant_risk
                round(row[3], 2),  # distance_from_home
                int(row[4]),       # transaction_velocity
                int(row[5]),       # is_international
                int(label)         # is_fraud
            ])
    print(f"Exported main dataset (500 rows) to: {dataset_path}")

    # 2. Export 2D Concentric Ring Kernel Benchmark dataset
    rng = np.random.RandomState(42)
    n_samples = 200
    n_fraud = n_samples // 3
    r_fraud = rng.uniform(0, 1.5, n_fraud)
    theta_fraud = rng.uniform(0, 2 * np.pi, n_fraud)
    x1_fraud = r_fraud * np.cos(theta_fraud) + rng.normal(0, 0.3, n_fraud)
    x2_fraud = r_fraud * np.sin(theta_fraud) + rng.normal(0, 0.3, n_fraud)
    
    n_legit = n_samples - n_fraud
    r_legit = rng.uniform(2.5, 4.0, n_legit)
    theta_legit = rng.uniform(0, 2 * np.pi, n_legit)
    x1_legit = r_legit * np.cos(theta_legit) + rng.normal(0, 0.3, n_legit)
    x2_legit = r_legit * np.sin(theta_legit) + rng.normal(0, 0.3, n_legit)
    
    X_2d = np.vstack([np.column_stack([x1_fraud, x2_fraud]), np.column_stack([x1_legit, x2_legit])])
    y_2d = np.hstack([np.ones(n_fraud), np.zeros(n_legit)])
    idx = rng.permutation(n_samples)
    X_2d, y_2d = X_2d[idx], y_2d[idx]

    kernel_dataset_path = os.path.join(os.getcwd(), 'fraudshield_2d_kernel_benchmark.csv')
    with open(kernel_dataset_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['feature_1', 'feature_2', 'is_fraud'])
        for row, label in zip(X_2d, y_2d):
            writer.writerow([round(row[0], 4), round(row[1], 4), int(label)])
    print(f"Exported 2D kernel benchmark dataset (200 rows) to: {kernel_dataset_path}")

    # 3. Export batch upload sample CSV (without labels)
    batch_sample_path = os.path.join(os.getcwd(), 'fraudshield_batch_sample.csv')
    with open(batch_sample_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(feature_names)
        sample_rows = [
            [45.00, 14, 0.15, 5.0, 1, 0],
            [2500.00, 2, 0.85, 150.0, 7, 1],
            [120.00, 10, 0.25, 12.0, 2, 0],
            [800.00, 3, 0.70, 80.0, 5, 1],
            [35.00, 16, 0.10, 3.0, 1, 0],
            [3200.00, 1, 0.90, 200.0, 8, 1],
            [67.50, 11, 0.20, 8.5, 1, 0],
            [950.00, 23, 0.65, 95.0, 6, 1],
            [28.00, 15, 0.12, 4.0, 1, 0],
            [1800.00, 4, 0.78, 120.0, 4, 1]
        ]
        writer.writerows(sample_rows)
    print(f"Exported batch evaluation sample to: {batch_sample_path}")

if __name__ == '__main__':
    export_csv_files()
