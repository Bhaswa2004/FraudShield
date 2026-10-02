"""
=============================================================================
SMS Spam Detection - Flask Web Application
=============================================================================
Loads the trained SVM model and TF-IDF vectorizer, then serves a web UI
where users can type an SMS message and get a SPAM / HAM prediction.

Run:  python app.py
Open: http://127.0.0.1:5000
=============================================================================
"""

import os
import re
import string

import joblib
from flask import Flask, render_template, request, jsonify

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = Flask(__name__)

# Paths to the saved model and vectorizer (produced by spam_svm.py)
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "output", "svm_spam_model.joblib")
VEC_PATH   = os.path.join(BASE_DIR, "output", "tfidf_vectorizer.joblib")

# Load model and vectorizer once at startup
model      = None
vectorizer = None


def load_artifacts():
    """Load the trained model and vectorizer from disk."""
    global model, vectorizer
    if not os.path.isfile(MODEL_PATH) or not os.path.isfile(VEC_PATH):
        raise FileNotFoundError(
            "Model files not found! Run  python spam_svm.py  first to train "
            "and save the model."
        )
    model      = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VEC_PATH)
    print(f"[OK] Model loaded from {MODEL_PATH}")
    print(f"[OK] Vectorizer loaded from {VEC_PATH}")


# ---------------------------------------------------------------------------
# Text preprocessing (same as spam_svm.py)
# ---------------------------------------------------------------------------
def preprocess_text(text: str) -> str:
    """Lowercase, remove punctuation, collapse whitespace."""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------------------------------------------------------------------
# Prediction helper
# ---------------------------------------------------------------------------
def predict_message(text: str) -> dict:
    """
    Predict whether a message is SPAM or HAM.
    Returns a dict with the label and the cleaned text.
    """
    cleaned    = preprocess_text(text)
    features   = vectorizer.transform([cleaned])
    prediction = model.predict(features)[0]
    label      = "SPAM" if prediction == 1 else "HAM"
    return {"label": label, "cleaned": cleaned}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """API endpoint: receive a message, return SPAM/HAM prediction as JSON."""
    data    = request.get_json(silent=True)
    message = data.get("message", "").strip() if data else ""

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    result = predict_message(message)
    return jsonify({
        "label":    result["label"],
        "cleaned":  result["cleaned"],
        "original": message,
    })


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    load_artifacts()
    print("\n  SMS Spam Detector is running!")
    print("  Open http://127.0.0.1:5000 in your browser.\n")
    app.run(debug=False, port=5000)
