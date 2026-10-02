# SMS Spam Detection using SVM

A machine learning project that classifies SMS messages as **Spam** or **Ham** (not spam) using Support Vector Machines.

## Dataset

**SMS Spam Collection Dataset** from [Kaggle / UCI ML Repository](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset)

- 5,572 SMS messages (4,825 ham, 747 spam — ~13.4 % spam)
- Download `spam.csv` from the link above and place it in this project folder.

## Project Structure

```
FraudShield/
├── spam_svm.py          # Main script (train, evaluate, tune, predict)
├── spam.csv             # Dataset (download from Kaggle)
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── output/              # Generated after running the script
    ├── class_distribution.png
    ├── confusion_matrix_best.png
    ├── kernel_comparison.png
    ├── svm_spam_model.joblib
    └── tfidf_vectorizer.joblib
```

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Make sure spam.csv is in the project folder

# 3. Run the script
python spam_svm.py
```

The script will:
1. Load and preprocess the data
2. Train three SVM classifiers (Linear, RBF, Polynomial)
3. Compare their performance
4. Tune the best kernel with GridSearchCV
5. Save plots to `output/` and the final model/vectorizer as `.joblib` files

## Results Summary

| Kernel     | Accuracy | Precision | Recall | F1-Score |
|------------|----------|-----------|--------|----------|
| Linear     | 0.9848   | 0.9925    | 0.8926 | 0.9399   |
| RBF        | 0.9785   | 0.9921    | 0.8456 | 0.9130   |
| Polynomial | 0.9390   | 1.0000    | 0.5436 | 0.7043   |

After hyperparameter tuning (GridSearchCV, 5-fold CV, F1 scoring, best `C=10`), the **Linear SVM** achieves:
- **F1-score: 0.9583** | Precision: 0.99 | Recall: 0.93 | Accuracy: 0.99

## Why Does a Linear Kernel Work Best for Text Data?

TF-IDF produces a **high-dimensional, sparse** feature space (up to 5,000 dimensions here). In high-dimensional spaces:

1. **Data is often linearly separable** — the "curse of dimensionality" actually helps classification because points are spread out, making it easier to find a separating hyperplane.
2. **Non-linear kernels add complexity without benefit** — RBF and polynomial kernels map features into an even higher-dimensional space, which is unnecessary when the data is already high-dimensional and roughly linearly separable.
3. **Linear kernels are faster** — training is O(n × d) rather than O(n²) or worse, making them practical for large vocabularies.
4. **Less overfitting risk** — with fewer hyper-parameters to tune (just C), a linear SVM generalises well on text data.

This is why linear SVMs (and similar linear models) are a standard baseline for text classification tasks like spam detection, sentiment analysis, and topic categorisation.

## Using the Saved Model

```python
import joblib

model      = joblib.load("output/svm_spam_model.joblib")
vectorizer = joblib.load("output/tfidf_vectorizer.joblib")

# predict_message() is also available if you import from spam_svm
from spam_svm import predict_message

result = predict_message("You won a free ticket! Call now!", model, vectorizer)
print(result)   # → SPAM
```

## Dependencies

- Python 3.8+
- pandas, scikit-learn, matplotlib, seaborn, joblib

## License

This project is for educational purposes (college project).
