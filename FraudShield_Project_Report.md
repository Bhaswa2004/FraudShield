# FRAUDSHIELD: FINANCIAL FRAUD INTELLIGENCE
## A Comprehensive Implementation of Unit 2 Classification Concepts: Linear Discriminants, Maximum-Margin Classifiers, and Kernel Methods

**Course Project Report**  
**Course**: Machine Learning Laboratory (Unit 2 Classification)  
**Academic Degree**: Bachelor of Technology in Computer Science & Engineering (3rd Year)  
**Student Name**: [Candidate Name]  
**Registration / Roll No**: [Register Number]  
**Supervisor / Guide**: [Faculty Guide Name]  
**Department**: Computer Science & Engineering  

---

## CERTIFICATE & DECLARATION

### Certificate of the Supervisor
This is to certify that the project report entitled **"FraudShield: Financial Fraud Intelligence"** submitted by **[Candidate Name]** (Registration No: **[Register Number]**) in partial fulfillment of the requirements for the degree of Bachelor of Technology in Computer Science and Engineering is a bonafide record of the research and practical implementation carried out under my supervision.

**Signature of Faculty Guide**: _______________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Date**: _______________

### Student Declaration
I hereby declare that this project report titled **"FraudShield: Financial Fraud Intelligence"** is an authentic record of my own work carried out under the academic guidance of **[Faculty Guide Name]**. The core concepts of Unit 2 classification—namely Linear Discriminants, Least-Squares Parameter Estimation, Linear Support Vector Machines, and Radial Basis Function (RBF) Kernels—have been visibly implemented with full mathematical transparency, without reliance on black-box neural networks, deep learning models, or ensemble trees.

**Signature of Candidate**: _______________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Date**: _______________

---

## ABSTRACT
In high-volume digital banking and card payment infrastructures, financial fraud detection is a mission-critical challenge characterized by extreme cost asymmetry and strict regulatory accountability. Traditional heuristic rule engines are rigid and vulnerable to evolving attack vectors, while contemporary deep neural networks operate as uninterpretable "black boxes", failing regulatory audits mandated by international banking frameworks (such as Basel III and GDPR Article 22).

This project presents **FraudShield**, an explainable financial fraud intelligence platform engineered to demonstrate core Unit 2 Machine Learning classification principles. The system implements a multi-model architecture incorporating:
1. A manually derived **Linear Discriminant Function** trained via closed-form ordinary least squares regression ($w = (X^T X)^{-1} X^T y$);
2. A maximum-margin **Linear Support Vector Machine (SVM)** exposing hyperplane weights, bias, support vectors, and margin width ($2 / \|w\|$);
3. A non-linear **Radial Basis Function (RBF) Kernel SVM** demonstrating the kernel trick on non-linearly separable fraud distributions; and
4. A probabilistic **Logistic Regression** baseline.

Rather than outputting opaque classifications, FraudShield provides full mathematical attribution by decomposing the discriminant score into exact per-feature contributions ($w_i \cdot x_i$). Experimental evaluation on a standardized 6-feature transaction space and a non-linear concentric ring benchmark reveals that while Linear SVM fails on non-linear geometries (67.0% accuracy, 138 support vectors), the RBF Kernel model attains **100.0% accuracy** (28 support vectors). Furthermore, the financial cost matrix is analyzed, highlighting why cyber-defense architectures must prioritize **Recall over Precision** to eradicate devastating False Negatives.

---

## TABLE OF CONTENTS
1. [Introduction](#chapter-1-introduction)
   - 1.1 Background & Context
   - 1.2 The Problem of Black-Box Models in Financial Security
   - 1.3 Objectives of the Project
   - 1.4 Scope and Constraints
2. [Theoretical Foundations & Mathematical Formulations](#chapter-2-theoretical-foundations--mathematical-formulations)
   - 2.1 Linear Discriminant Functions
   - 2.2 Parameter Estimation via Least-Squares Classification
   - 2.3 Maximum-Margin Hyperplanes & Linear SVM
   - 2.4 The Kernel Trick & Radial Basis Function (RBF) Kernels
   - 2.5 Probabilistic Modeling via Logistic Regression
3. [System Design & Architectural Specification](#chapter-3-system-design--architectural-specification)
   - 3.1 Multi-Tier Modular Architecture
   - 3.2 Feature Vector Design ($\mathbb{R}^6$ Space)
   - 3.3 Database Schema & Audit Logging
   - 3.4 RESTful API & WebSocket Specifications
4. [Implementation Methodology](#chapter-4-implementation-methodology)
   - 4.1 Synthetic Data Generation & Z-Score Standardization
   - 4.2 Closed-Form Least-Squares Implementation
   - 4.3 Linear & Non-Linear SVM Implementation
   - 4.4 HTML5 Canvas Dynamic Decision Boundary Visualizer
5. [Experimental Results, Analysis & Viva Discussion](#chapter-5-experimental-results-analysis--viva-discussion)
   - 5.1 Model Evaluation Metrics on Banking Test Split
   - 5.2 Non-Linear Benchmark: Linear vs. RBF Kernel Performance
   - 5.3 Feature Contribution Attribution & Explainability
   - 5.4 The Cost Asymmetry: False Negatives vs. False Positives
6. [Conclusion & Future Directions](#chapter-6-conclusion--future-directions)
7. [References](#references)
8. [Appendix: Key Mathematical Derivations & Code Extracts](#appendix-key-mathematical-derivations--code-extracts)

---

## CHAPTER 1: INTRODUCTION

### 1.1 Background & Context
The digital transformation of the global financial sector has led to an exponential expansion in electronic payment processing, online banking transactions, and card-not-present (CNP) purchases. Concurrently, criminal fraud syndicates have evolved sophisticated countermeasures, resulting in billions of dollars in annual losses. Traditional financial security suites have historically relied upon hand-crafted heuristic rule engines (e.g., *"flag transaction if amount > $5000 and time is between 2:00 AM and 4:00 AM"*). However, static heuristics exhibit high false-alarm rates and are incapable of detecting complex behavioral drifts or subtle cross-feature correlations.

### 1.2 The Problem of Black-Box Models in Financial Security
While modern machine learning techniques offer significant pattern recognition capabilities, enterprise adoption in banking faces severe regulatory hurdles. In recent years, data science initiatives have frequently deployed Deep Neural Networks (DNNs), Random Forests, and XGBoost classifiers. While these architectures demonstrate high numerical accuracy, they act as uninterpretable black boxes. Regulatory bodies—including the Reserve Bank of India (RBI), the European Union General Data Protection Regulation (GDPR Article 22), and the Basel Committee on Banking Supervision—strictly mandate that financial institutions must be capable of providing explainable audit trails justifying why a customer's legitimate card was blocked or how a transaction was flagged as fraudulent.

### 1.3 Objectives of the Project
The primary goal of FraudShield is to build an auditable, mathematically transparent classification system that bridges academic machine learning theory (specifically Unit 2: Linear Discriminants, SVMs, and Kernel Methods) with practical software engineering. The specific objectives include:
- Implement a linear discriminant classifier from first principles using NumPy, estimating parameters via the normal equations of least-squares classification.
- Deconstruct the classification decision into individual feature contribution terms ($w_i \cdot x_i$), enabling real-time visual explainability.
- Expose the geometric internals of Support Vector Machines, including hyperplane weight vectors, intercept, support vector counts, and margin width.
- Demonstrate the necessity of the Kernel Trick by visualizing decision boundaries on a non-linearly separable benchmark dataset.
- Analyze the economic impact of classification errors, focusing on the cost asymmetry between False Negatives (missed fraud) and False Positives (customer friction).

### 1.4 Scope and Constraints
To preserve academic rigor and maintain strict compliance with syllabus requirements, this project explicitly avoids deep learning, convolutional neural networks, transformers, large language models, random forests, and gradient boosting trees. All modeling is strictly confined to Unit 2 statistical classification theory.

---

## CHAPTER 2: THEORETICAL FOUNDATIONS & MATHEMATICAL FORMULATIONS

### 2.1 Linear Discriminant Functions
A linear discriminant function is a linear combination of input features that partitions an input space $\mathbb{R}^d$ into distinct classification regions. For a binary classification setting where targets $y \in \{0, 1\}$, the discriminant function is formally defined as:

$$g(\mathbf{x}) = \mathbf{w}^T \mathbf{x} + b = \sum_{i=1}^d (w_i \cdot x_i) + b$$

Here, $\mathbf{w} = [w_1, w_2, \dots, w_d]^T$ represents the weight vector (which defines the normal orientation of the separating hyperplane), $\mathbf{x} = [x_1, x_2, \dots, x_d]^T$ is the feature vector, and $b$ represents the scalar bias or threshold offset.

The decision rule classifies an input vector $\mathbf{x}$ into class 1 (Fraud) if $g(\mathbf{x}) \ge 0.5$ and class 0 (Legitimate) if $g(\mathbf{x}) < 0.5$. A critical property of linear discriminants is feature additivity: each term $w_i \cdot x_i$ represents the signed scalar contribution of feature $i$ toward the final verdict.

### 2.2 Parameter Estimation via Least-Squares Classification
Linear classification can be viewed through the lens of ordinary regression. By augmenting the feature vector with a constant bias term $\mathbf{x}_{aug} = [\mathbf{x}^T, 1]^T \in \mathbb{R}^{d+1}$, we express the system as:

$$X_{aug} = [X, \mathbf{1}_N] \in \mathbb{R}^{N \times (d+1)}, \quad \mathbf{w}_{aug} = [\mathbf{w}^T, b]^T \in \mathbb{R}^{d+1}$$

The least-squares objective minimizes the sum of squared differences between continuous predictions and categorical target labels $y \in \{0, 1\}$:

$$J(\mathbf{w}_{aug}) = \|X_{aug} \mathbf{w}_{aug} - \mathbf{y}\|^2 = (X_{aug} \mathbf{w}_{aug} - \mathbf{y})^T (X_{aug} \mathbf{w}_{aug} - \mathbf{y})$$

Setting the gradient $\nabla_{\mathbf{w}_{aug}} J = 0$ yields the classic normal equations, solved using the Moore-Penrose pseudo-inverse:

$$\mathbf{w}_{aug} = (X_{aug}^T X_{aug})^{-1} X_{aug}^T \mathbf{y}$$

> **Viva Examination Note**: While computationally efficient and closed-form, least-squares classification has a well-known vulnerability: outliers positioned deep within their correct class regions generate large squared error penalties, which can paradoxically rotate and displace the decision hyperplane away from optimal separation.

### 2.3 Maximum-Margin Hyperplanes & Linear Support Vector Machines
To address the limitations of least-squares classification, Vapnik introduced Support Vector Machines (SVM). Rather than minimizing residual error across all samples, SVM identifies the optimal hyperplane that maximizes the geometric margin between classes.

The primal optimization problem for a linearly separable dataset is formulated as:

$$\min_{\mathbf{w}, b} \frac{1}{2} \|\mathbf{w}\|^2 \quad \text{subject to } y_i (\mathbf{w}^T \mathbf{x}_i + b) \ge 1, \quad \forall i \in \{1, \dots, N\}$$

The geometric margin width $M$ represents the perpendicular distance between the two supporting bounding planes ($\mathbf{w}^T \mathbf{x} + b = +1$ and $\mathbf{w}^T \mathbf{x} + b = -1$):

$$M = \frac{2}{\|\mathbf{w}\|_2}$$

Data points $\mathbf{x}_i$ that satisfy $y_i(\mathbf{w}^T \mathbf{x}_i + b) = 1$ are termed **Support Vectors**. All other training samples have zero influence on the position of the separating plane. This property confers extreme structural robustness against non-boundary outliers.

### 2.4 The Kernel Trick & Radial Basis Function (RBF) Kernels
When the true decision boundary is non-linear, no linear hyperplane in $\mathbb{R}^d$ can achieve acceptable separation without catastrophic misclassification. The Kernel Trick addresses this by implicitly projecting input vectors $\mathbf{x}$ into a higher- (or infinite-) dimensional Hilbert space $\mathcal{H}$ via a non-linear mapping $\Phi(\mathbf{x})$:

$$\Phi: \mathbb{R}^d \to \mathcal{H}, \quad \text{where } \dim(\mathcal{H}) \gg d$$

By Mercer's Theorem, the inner product in $\mathcal{H}$ can be computed directly in the low-dimensional input space using a valid positive semi-definite kernel function $K(\mathbf{x}, \mathbf{x}') = \langle\Phi(\mathbf{x}), \Phi(\mathbf{x}')\rangle$. FraudShield implements the Radial Basis Function (RBF) kernel:

$$K(\mathbf{x}, \mathbf{x}') = \exp\left(-\gamma \|\mathbf{x} - \mathbf{x}'\|^2\right)$$

The parameter $\gamma = \frac{1}{2\sigma^2}$ controls the radius of influence of each support vector. High values of $\gamma$ create localized, tightly-fitted boundaries, while low values produce smooth, generalized contours.

### 2.5 Probabilistic Modeling via Logistic Regression
To complement geometric margin distances with calibrated posterior probabilities, FraudShield incorporates Logistic Regression as a baseline. The log-odds (logit) of fraud are modeled as a linear combination of features, mapped onto $[0, 1]$ via the standard sigmoid function:

$$P(y = 1 \mid \mathbf{x}) = \sigma(\mathbf{w}^T \mathbf{x} + b) = \frac{1}{1 + \exp(-(\mathbf{w}^T \mathbf{x} + b))}$$

---

## CHAPTER 3: SYSTEM DESIGN & ARCHITECTURAL SPECIFICATION

### 3.1 Multi-Tier Modular Architecture
FraudShield adheres to strict enterprise separation of concerns, structured into five decoupled layers:
- **Data Layer (`/data_layer`)**: Handles synthetic data generation, manual feature scaling, and CSV streaming.
- **Model Layer (`/model_layer`)**: Houses all mathematical classifier implementations, training pipelines, and 2D grid generation.
- **Storage Layer (`/db`)**: Manages SQLite persistence for audit logs and JWT user credential storage.
- **API Layer (`/api_layer`)**: Exposes asynchronous REST endpoints and WebSocket alert channels via FastAPI.
- **Presentation Layer (`/frontend`)**: Single-page dark-mode web application featuring real-time CSS charts and HTML5 Canvas boundary plots.

### 3.2 Feature Vector Design ($\mathbb{R}^6$ Space)
The primary transaction feature space consists of six continuous and categorical variables:
1. `amount` (Continuous, $): Exponential tail. Normal purchases: $10–$500; Fraud purchases: $100–$10,000.
2. `hour` (Discrete, 0–23): Hour of day. Fraud peaks during late-night / off-peak hours (00:00–05:00).
3. `merchant_risk` (Continuous, [0, 1]): Vendor risk score sampled from Beta distribution: $\text{Beta}(7,3)$ for fraud, $\text{Beta}(2,8)$ for legitimate.
4. `distance_from_home` (Continuous, km): Geographical distance from cardholder billing address. Exponentially higher for fraud.
5. `transaction_velocity` (Integer, $\ge 1$): Number of charges attempted in the preceding 60 minutes. Sampled via Poisson distribution.
6. `is_international` (Binary, $\{0, 1\}$): Cross-border payment flag (60% occurrence in fraud vs 10% in normal transactions).

### 3.3 Database Schema & Audit Logging
The SQLite database (`fraudshield.db`) maintains an immutable audit ledger across two tables:
- **`transactions` Table**: Stores unique transaction ID, ISO timestamp, 6 raw feature values, discriminant raw score, discriminant verdict, serialized JSON feature contributions, SVM decision score, SVM verdict, serialized JSON support vector details, and final fraud flag.
- **`users` Table**: Manages administrative accounts with username, salt-hashed password (bcrypt), creation date, and last login timestamp.

### 3.4 RESTful API & WebSocket Specifications
The FastAPI application exposes the following endpoints:
- `POST /api/predict`: Consumes JSON feature payload, executes all 4 classifiers, logs to DB, broadcasts WebSocket alert if fraud, and returns full math breakdowns.
- `POST /api/batch`: Accepts `multipart/form-data` CSV, processes transactions in a streaming loop, and returns bulk classifications with fraud summary counts.
- `GET /api/boundary?kernel=linear|rbf`: Generates an $80 \times 80$ meshgrid over the 2D benchmark dataset, computing decision values $Z$ for canvas heatmap rendering.
- `GET /api/metrics`: Returns accuracy, precision, recall, F1, and full confusion matrices evaluated on the 20% stratified test split.
- `WebSocket /ws/alerts`: Full-duplex WebSocket connection delivering instant push notifications to active dashboard sessions.

---

## CHAPTER 4: IMPLEMENTATION METHODOLOGY

### 4.1 Synthetic Data Generation & Manual Z-Score Standardization
To eliminate artificial scaling bias, features are normalized using a custom `FeatureScaler` implemented in NumPy without scikit-learn dependencies. Means $\mu_j$ and standard deviations $\sigma_j$ are computed strictly on the training partition:

$$z_{ij} = \frac{x_{ij} - \mu_j}{\sigma_j + 10^{-8}}$$

### 4.2 Closed-Form Least-Squares Implementation
The `DiscriminantClassifier` class performs augmentation and solves the normal equations using `np.linalg.pinv` to guarantee numerical stability even in the presence of collinearity:

```python
X_aug = np.hstack([X, np.ones((X.shape[0], 1))])
w_aug = np.linalg.pinv(X_aug.T @ X_aug) @ X_aug.T @ y
self.weights = w_aug[:-1]
self.bias = w_aug[-1]
```

### 4.3 Linear & Non-Linear SVM Implementation
The `LinearSVMClassifier` and `RBFSVMClassifier` classes wrap scikit-learn's `SVC` primitives while exposing private attributes required for educational viva inspection: `decision_function()`, `coef_`, `intercept_`, and `n_support_`.

### 4.4 HTML5 Canvas Dynamic Decision Boundary Visualizer
To demonstrate the kernel trick visually, `ModelManager` constructs a 200-sample concentric circular benchmark in $\mathbb{R}^2$ (fraud points in an inner circle of radius $r < 1.5$, legitimate points in an outer ring of radius $2.5 < r < 4.0$). The browser executes a bilinear contour traversal across an $80 \times 80$ decision grid $Z$, rendering the separating zero-level set ($Z = 0$) in amber gold alongside highlighted support vector markers.

---

## CHAPTER 5: EXPERIMENTAL RESULTS, ANALYSIS & VIVA DISCUSSION

### 5.1 Model Evaluation Metrics on Banking Test Split
The classifiers were evaluated on an 80/20 stratified train/test split (400 training samples, 100 test samples containing 80 legitimate and 20 fraud transactions). Table 5.1 details the empirical performance:

| Classifier Model | Accuracy | Precision | Recall | F1-Score | True Neg / False Pos | False Neg / True Pos |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Linear Discriminant** | 99.0% | 100.0% | 95.0% | 97.4% | 80 / 0 | 1 / 19 |
| **Linear SVM** | 99.0% | 100.0% | 95.0% | 97.4% | 80 / 0 | 1 / 19 |
| **RBF Kernel SVM** | **100.0%** | **100.0%** | **100.0%** | **100.0%** | **80 / 0** | **0 / 20** |
| **Logistic Regression** | 99.0% | 100.0% | 95.0% | 97.4% | 80 / 0 | 1 / 19 |

*Table 5.1: Comparative classification performance across models on held-out test split.*

### 5.2 Non-Linear Benchmark: Linear vs RBF Kernel Performance
When evaluated against the 2D concentric ring dataset, the fundamental limitation of linear classification becomes mathematically apparent:
- **Linear Kernel SVM**: Attains only **67.0% Accuracy**. Because a straight line cannot encapsulate a central cluster without bisecting the surrounding ring, 138 out of 200 data points (69%) are forced to become support vectors due to margin boundary violations.
- **RBF Kernel SVM**: Attains **100.0% Accuracy**. By projecting inputs into an infinite-dimensional RKHS, the model constructs a smooth, closed circular contour enclosing the fraud cluster, requiring only 28 support vectors (14%).

### 5.3 Feature Contribution Attribution & Explainability
Analyzing the learned weights $\mathbf{w}$ across linear models reveals that `merchant_risk` ($w = +1.4446$) and `distance_from_home` ($w = +0.6755$) exert the strongest positive influence toward fraud verdicts, followed by `amount` ($+0.6461$) and `transaction_velocity` ($+0.5700$). In contrast, `hour` ($-0.0493$) exerts a mild negative bias during standard daytime hours, confirming intuitive banking logic.

### 5.4 The Cost Asymmetry: False Negatives vs False Positives
In standard machine learning benchmarks, models are evaluated under symmetric zero-one loss. However, in financial cyber-defense, errors are profoundly asymmetric:
- **False Positive (FP)**: A legitimate purchase is flagged. The cardholder experiences slight friction (e.g., verifying identity via SMS OTP). Financial cost is negligible (approx. $25 in customer support overhead).
- **False Negative (FN)**: A fraudulent charge goes undetected. The fraudster completes the unauthorized transfer, resulting in direct balance depletion, interchange chargeback penalties, forensic investigation costs, and reputation damage (historically estimated at 3.0x the transaction amount).

Consequently, the optimal financial operating threshold must maximize Recall ($\text{Sensitivity} = \frac{TP}{TP + FN}$), accepting minor reductions in Precision to drive False Negatives strictly to zero.

---

## CHAPTER 6: CONCLUSION & FUTURE DIRECTIONS

### 6.1 Conclusion
FraudShield successfully operationalizes the theoretical constructs of Unit 2 Machine Learning into an auditable, enterprise-grade classification engine. By computing closed-form least-squares solutions, displaying maximum-margin support vector hyperplanes, and visually demonstrating kernel-induced non-linear separation on dynamic HTML5 canvases, the project establishes that explainable classical classification provides rigorous mathematical accountability that opaque deep-learning models cannot match.

### 6.2 Future Work
Future enhancements planned for FraudShield include:
- **Streaming Pipeline Integration**: Connecting the FastAPI backend to Apache Kafka and Redis for distributed sub-millisecond payment stream evaluation.
- **Kaggle European Dataset Ingestion**: Validating the algorithms on the benchmark 284,807 European cardholder transaction dataset with PCA-transformed features.
- **Automated Grid Search & Cross-Validation**: Implementing real-time hyperparameter tuning for SVM slack penalty $C$ and RBF bandwidth $\gamma$.

---

## REFERENCES
1. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer, New York. (Chapter 4: Linear Models for Classification).
2. Duda, R. O., Hart, P. E., & Stork, D. G. (2001). *Pattern Classification* (2nd ed.). John Wiley & Sons. (Chapter 5: Linear Discriminant Functions).
3. Vapnik, V. (1998). *Statistical Learning Theory*. Wiley-Interscience, New York.
4. Cortes, C., & Vapnik, V. (1995). Support-vector networks. *Machine Learning*, 20(3), 273-297.
5. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer.
6. Basel Committee on Banking Supervision. (2021). *Sound Practices: Implications of fintech developments for banks and bank supervisors*. Bank for International Settlements.

---

## APPENDIX: KEY MATHEMATICAL DERIVATIONS & CODE EXTRACTS

### Appendix A: Discriminant Calculation Snippet (`model_layer/discriminant.py`)
```python
def score_single(self, x_scaled: np.ndarray, feature_names: list[str]) -> dict:
    raw_score = float(np.dot(self.weights, x_scaled) + self.bias)
    verdict = 'FRAUD' if raw_score >= self.threshold else 'LEGITIMATE'
    weighted_terms = {
        feature_names[i]: {
            'weight': float(self.weights[i]),
            'scaled_value': float(x_scaled[i]),
            'contribution': float(self.weights[i] * x_scaled[i])
        } for i in range(len(feature_names))
    }
    return {
        'model': 'discriminant_function',
        'raw_score': raw_score,
        'threshold': self.threshold,
        'verdict': verdict,
        'weighted_terms': weighted_terms,
        'bias': float(self.bias),
        'formula': 'g(x) = w·x + b'
    }
```
