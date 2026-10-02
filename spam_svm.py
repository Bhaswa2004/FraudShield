"""
=============================================================================
SMS Spam Detection using Support Vector Machine (SVM)
=============================================================================
College Project - Machine Learning

This script:
  1. Loads and cleans the SMS Spam Collection Dataset (spam.csv)
  2. Preprocesses text (lowercase, remove punctuation/extra whitespace)
  3. Converts text to TF-IDF features
  4. Trains three SVM classifiers (Linear, RBF, Polynomial kernels)
  5. Evaluates and compares them (accuracy, precision, recall, F1, confusion matrix)
  6. Tunes the best kernel with GridSearchCV (5-fold CV, F1 scoring)
  7. Saves visualizations as PNG files
  8. Provides a predict_message() helper function
  9. Saves the final model and vectorizer with joblib
=============================================================================
"""

# -- Imports -----------------------------------------------------------------
import os
import sys
import re
import string

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")                       # non-interactive backend (safe for scripts)
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
import joblib

# -- Configuration -----------------------------------------------------------
DATA_FILE      = "spam.csv"          # expected in the same folder as this script
RANDOM_STATE   = 42
TEST_SIZE      = 0.20               # 80/20 split
MAX_FEATURES   = 5000               # TF-IDF vocabulary cap
OUTPUT_DIR     = "output"           # folder for PNGs and saved models


# =============================================================================
# SECTION 1 - LOAD THE DATASET
# =============================================================================
def load_data(filepath: str) -> pd.DataFrame:
    """
    Load spam.csv, keep only the label and message columns, and encode
    ham -> 0, spam -> 1.
    """
    if not os.path.isfile(filepath):
        print("=" * 65)
        print("  ERROR: spam.csv not found in the project folder!")
        print("=" * 65)
        print()
        print("  How to get the dataset:")
        print("  1. Go to https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset")
        print("  2. Click 'Download' (you may need a free Kaggle account).")
        print("  3. Extract the ZIP and copy  spam.csv  into:")
        print(f"     {os.path.abspath(os.path.dirname(filepath) or '.')}")
        print()
        sys.exit(1)

    # The CSV has some extra unnamed columns; latin-1 encoding handles special chars
    df = pd.read_csv(filepath, encoding="latin-1")

    # Keep only the first two columns (v1 = label, v2 = message text)
    df = df.iloc[:, :2]
    df.columns = ["label", "message"]

    # Encode labels: ham -> 0, spam -> 1
    df["label"] = df["label"].map({"ham": 0, "spam": 1})

    print(f"[OK] Dataset loaded: {len(df)} messages  "
          f"(ham={len(df[df.label==0])}, spam={len(df[df.label==1])})")
    return df


# =============================================================================
# SECTION 2 - TEXT PREPROCESSING
# =============================================================================
def preprocess_text(text: str) -> str:
    """
    Clean a single SMS message:
      * convert to lowercase
      * remove punctuation
      * collapse extra whitespace
    """
    text = text.lower()                                  # lowercase
    text = text.translate(str.maketrans("", "", string.punctuation))  # remove punctuation
    text = re.sub(r"\s+", " ", text).strip()             # collapse whitespace
    return text


# =============================================================================
# SECTION 3 - FEATURE EXTRACTION (TF-IDF)
# =============================================================================
def build_tfidf(X_train, X_test, max_features=MAX_FEATURES):
    """
    Fit a TfidfVectorizer on the training data and transform both sets.
    Returns the fitted vectorizer and the sparse TF-IDF matrices.
    """
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=max_features,
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf  = vectorizer.transform(X_test)

    print(f"[OK] TF-IDF matrix shape: {X_train_tfidf.shape} (train), "
          f"{X_test_tfidf.shape} (test)")
    return vectorizer, X_train_tfidf, X_test_tfidf


# =============================================================================
# SECTION 4 - TRAIN THREE SVM KERNELS & COMPARE
# =============================================================================
def train_and_evaluate(X_train, y_train, X_test, y_test):
    """
    Train Linear, RBF, and Polynomial SVM classifiers.
    Returns a dict  {kernel_name: {"model": ..., "metrics": {...}}}
    """
    kernels = {
        "Linear":     SVC(kernel="linear",  C=1.0, random_state=RANDOM_STATE),
        "RBF":        SVC(kernel="rbf",     C=1.0, gamma="scale", random_state=RANDOM_STATE),
        "Polynomial": SVC(kernel="poly",    C=1.0, degree=3, gamma="scale", random_state=RANDOM_STATE),
    }

    results = {}
    for name, clf in kernels.items():
        print(f"\n-- Training SVM ({name} kernel) --")
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        acc  = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec  = recall_score(y_test, y_pred)
        f1   = f1_score(y_test, y_pred)
        cm   = confusion_matrix(y_test, y_pred)

        results[name] = {
            "model":   clf,
            "y_pred":  y_pred,
            "metrics": {"Accuracy": acc, "Precision": prec, "Recall": rec, "F1": f1},
            "cm":      cm,
        }

        print(f"   Accuracy : {acc:.4f}")
        print(f"   Precision: {prec:.4f}")
        print(f"   Recall   : {rec:.4f}")
        print(f"   F1-score : {f1:.4f}")
        print(f"   Confusion matrix:\n{cm}")

    return results


# =============================================================================
# SECTION 5 - HYPERPARAMETER TUNING (GridSearchCV)
# =============================================================================
def tune_best_kernel(X_train, y_train, best_kernel: str):
    """
    Use GridSearchCV with 5-fold stratified CV (scoring=F1) to tune C
    (and gamma for RBF) for the winning kernel.
    Returns the best estimator.
    """
    print(f"\n== Tuning {best_kernel} kernel with GridSearchCV (F1, 5-fold CV) ==")

    if best_kernel == "Linear":
        param_grid = {"C": [0.01, 0.1, 1, 10, 100]}
        base_svm = SVC(kernel="linear", random_state=RANDOM_STATE)
    elif best_kernel == "RBF":
        param_grid = {
            "C":     [0.1, 1, 10, 100],
            "gamma": ["scale", "auto", 0.01, 0.1],
        }
        base_svm = SVC(kernel="rbf", random_state=RANDOM_STATE)
    else:  # Polynomial
        param_grid = {
            "C":      [0.1, 1, 10],
            "degree": [2, 3, 4],
            "gamma":  ["scale", "auto"],
        }
        base_svm = SVC(kernel="poly", random_state=RANDOM_STATE)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    grid = GridSearchCV(
        base_svm,
        param_grid,
        scoring="f1",
        cv=cv,
        n_jobs=-1,
        verbose=1,
    )
    grid.fit(X_train, y_train)

    print(f"   Best params : {grid.best_params_}")
    print(f"   Best CV F1  : {grid.best_score_:.4f}")
    return grid.best_estimator_


# =============================================================================
# SECTION 6 - VISUALIZATIONS
# =============================================================================
def plot_class_distribution(df, output_dir):
    """Bar chart showing how many Ham vs Spam messages are in the dataset."""
    counts = df["label"].value_counts().sort_index()
    labels = ["Ham (0)", "Spam (1)"]
    colors = ["#4CAF50", "#F44336"]

    plt.figure(figsize=(6, 4))
    bars = plt.bar(labels, counts.values, color=colors, edgecolor="black")
    for bar, val in zip(bars, counts.values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
                 str(val), ha="center", fontweight="bold")
    plt.title("Class Distribution (Ham vs Spam)", fontsize=14)
    plt.ylabel("Number of Messages")
    plt.tight_layout()
    path = os.path.join(output_dir, "class_distribution.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[OK] Saved {path}")


def plot_confusion_matrix(cm, kernel_name, output_dir):
    """Heatmap of the confusion matrix for the best model."""
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Ham", "Spam"], yticklabels=["Ham", "Spam"])
    plt.title(f"Confusion Matrix - Best Model ({kernel_name} SVM)", fontsize=13)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    path = os.path.join(output_dir, "confusion_matrix_best.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[OK] Saved {path}")


def plot_kernel_comparison(results, output_dir):
    """Grouped bar chart comparing accuracy, precision, recall, F1 across kernels."""
    metric_names = ["Accuracy", "Precision", "Recall", "F1"]
    kernel_names = list(results.keys())
    x = np.arange(len(metric_names))
    width = 0.25

    plt.figure(figsize=(9, 5))
    for i, kernel in enumerate(kernel_names):
        vals = [results[kernel]["metrics"][m] for m in metric_names]
        plt.bar(x + i * width, vals, width, label=kernel)

    plt.xticks(x + width, metric_names)
    plt.ylim(0.75, 1.02)
    plt.ylabel("Score")
    plt.title("SVM Kernel Comparison", fontsize=14)
    plt.legend()
    plt.tight_layout()
    path = os.path.join(output_dir, "kernel_comparison.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[OK] Saved {path}")


# =============================================================================
# SECTION 7 - PREDICTION FUNCTION
# =============================================================================
def predict_message(text: str, model, vectorizer) -> str:
    """
    Predict whether a single SMS message is SPAM or HAM.

    Parameters
    ----------
    text : str          - the raw SMS message
    model               - trained SVM classifier
    vectorizer          - fitted TfidfVectorizer

    Returns
    -------
    str  "SPAM" or "HAM"
    """
    cleaned = preprocess_text(text)
    features = vectorizer.transform([cleaned])
    prediction = model.predict(features)[0]
    return "SPAM" if prediction == 1 else "HAM"


# =============================================================================
# SECTION 8 - MAIN PIPELINE
# =============================================================================
def main():
    # -- Create output directory ---------------------------------------------
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # -- 1. Load data --------------------------------------------------------
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path  = os.path.join(script_dir, DATA_FILE)
    df = load_data(data_path)

    # -- 2. Preprocess text --------------------------------------------------
    print("\n-- Preprocessing text --")
    df["message"] = df["message"].apply(preprocess_text)
    print(f"[OK] Text cleaned. Sample:\n   '{df['message'].iloc[0]}'")

    # -- 3. Stratified train-test split --------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        df["message"], df["label"],
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=df["label"],       # preserve the ~13% spam ratio in both sets
    )
    print(f"\n[OK] Train/Test split: {len(X_train)} train, {len(X_test)} test")

    # -- 4. TF-IDF feature extraction ---------------------------------------
    vectorizer, X_train_tfidf, X_test_tfidf = build_tfidf(X_train, X_test)

    # -- 5. Train & compare three kernels ------------------------------------
    results = train_and_evaluate(X_train_tfidf, y_train, X_test_tfidf, y_test)

    # -- 6. Identify best kernel by F1 ---------------------------------------
    best_kernel = max(results, key=lambda k: results[k]["metrics"]["F1"])
    print(f"\n[*] Best kernel (by F1): {best_kernel} "
          f"(F1 = {results[best_kernel]['metrics']['F1']:.4f})")

    # -- 7. Hyperparameter tuning --------------------------------------------
    tuned_model = tune_best_kernel(X_train_tfidf, y_train, best_kernel)

    # Evaluate tuned model on the test set
    y_pred_tuned = tuned_model.predict(X_test_tfidf)
    print("\n-- Tuned Model - Test Set Results --")
    print(classification_report(y_test, y_pred_tuned, target_names=["Ham", "Spam"]))

    tuned_cm = confusion_matrix(y_test, y_pred_tuned)
    tuned_f1 = f1_score(y_test, y_pred_tuned)
    print(f"   Tuned F1: {tuned_f1:.4f}")

    # -- 8. Visualizations --------------------------------------------------
    print("\n-- Generating visualizations --")
    plot_class_distribution(df, OUTPUT_DIR)
    plot_confusion_matrix(tuned_cm, best_kernel, OUTPUT_DIR)
    plot_kernel_comparison(results, OUTPUT_DIR)

    # -- 9. Save model & vectorizer ------------------------------------------
    model_path = os.path.join(OUTPUT_DIR, "svm_spam_model.joblib")
    vec_path   = os.path.join(OUTPUT_DIR, "tfidf_vectorizer.joblib")
    joblib.dump(tuned_model, model_path)
    joblib.dump(vectorizer,  vec_path)
    print(f"\n[OK] Model saved  -> {model_path}")
    print(f"[OK] Vectorizer saved -> {vec_path}")

    # -- 10. Demo predictions ------------------------------------------------
    demo_messages = [
        "Hey, are we still meeting for lunch tomorrow?",
        "WINNER!! You have been selected for a $1000 prize! Call now!",
        "Please submit your assignment by Friday.",
        "Congratulations! You've won a free iPhone. Click here to claim.",
        "Can you pick up some milk on your way home?",
    ]

    print("\n======================================================")
    print("  DEMO - predict_message() on 5 example messages")
    print("======================================================")
    for msg in demo_messages:
        label = predict_message(msg, tuned_model, vectorizer)
        print(f"  [{label:4s}]  {msg}")

    print("\n[OK] Done! Check the 'output/' folder for PNGs and saved models.")


# -- Entry point -------------------------------------------------------------
if __name__ == "__main__":
    main()
