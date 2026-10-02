import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def create_report():
    doc = Document()

    # Set Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Style definitions
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Times New Roman'
    font_normal.size = Pt(12)
    font_normal.color.rgb = RGBColor(30, 41, 59) # Slate 800

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(24)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
        p.paragraph_format.space_before = Pt(36)
        p.paragraph_format.space_after = Pt(12)
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(14)
        run.font.italic = True
        run.font.color.rgb = RGBColor(71, 85, 105) # Slate 600
        p.paragraph_format.space_after = Pt(24)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42)
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 58, 138) # Dark blue
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(51, 65, 85)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        return p

    def add_body(text, space_after=6, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.bold = True
            r_pre.font.color.rgb = RGBColor(15, 23, 42)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11.5)
        r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.bold = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        return p

    def add_code_block(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Inches(0.4)
        run = p.add_run(text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    # ==========================================
    # 1. COVER PAGE
    # ==========================================
    add_title("FRAUDSHIELD: FINANCIAL FRAUD INTELLIGENCE")
    add_subtitle("A Comprehensive Implementation of Unit 2 Classification Concepts:\nLinear Discriminants, Maximum-Margin Classifiers, and Kernel Methods")

    p_cover_meta = doc.add_paragraph()
    p_cover_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cover_meta.paragraph_format.space_before = Pt(48)
    p_cover_meta.paragraph_format.space_after = Pt(24)
    r = p_cover_meta.add_run("A Project Report Submitted in Partial Fulfillment of the Requirements for the Award of the Degree of\n\nBACHELOR OF TECHNOLOGY\nin\nCOMPUTER SCIENCE AND ENGINEERING")
    r.font.name = 'Arial'
    r.font.size = Pt(12)
    r.font.bold = True

    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_before = Pt(36)
    p_by.paragraph_format.space_after = Pt(12)
    r_by = p_by.add_run("Submitted by:\n[STUDENT NAME] (Reg. No: [REGISTER NUMBER])\n3rd Year B.Tech CSE\n\nUnder the Supervision of:\n[FACULTY GUIDE NAME]\nDepartment of Computer Science & Engineering\n[COLLEGE / UNIVERSITY NAME]\nAcademic Year 2025 – 2026")
    r_by.font.name = 'Times New Roman'
    r_by.font.size = Pt(11)

    doc.add_page_break()

    # ==========================================
    # 2. CERTIFICATE & DECLARATION
    # ==========================================
    add_h1("CERTIFICATE & DECLARATION")
    add_h2("Certificate of the Supervisor")
    add_body("This is to certify that the project report entitled 'FraudShield: Financial Fraud Intelligence' submitted by [STUDENT NAME] (Registration No: [REGISTER NUMBER]) in partial fulfillment of the requirements for the degree of Bachelor of Technology in Computer Science and Engineering is a bonafide record of the work carried out under my guidance and supervision.")
    add_body("\n\nSignature of Faculty Guide: ______________________      Date: ____________")

    add_h2("Student Declaration")
    add_body("I hereby declare that this project report titled 'FraudShield: Financial Fraud Intelligence' is an authentic record of my own work carried out under the guidance of [FACULTY GUIDE NAME]. The concepts of Unit 2 classification—namely Linear Discriminants, Least-Squares Estimation, Linear Support Vector Machines, and Radial Basis Function (RBF) Kernels—have been implemented with full mathematical transparency, without reliance on black-box neural networks, deep learning models, or ensemble trees.")
    add_body("\n\nSignature of Candidate: ______________________         Date: ____________")

    doc.add_page_break()

    # ==========================================
    # 3. ABSTRACT
    # ==========================================
    add_h1("ABSTRACT")
    add_body("In high-volume digital banking and card payment infrastructures, financial fraud detection is a mission-critical challenge characterized by extreme cost asymmetry and strict regulatory accountability. Traditional heuristic rule engines are rigid and vulnerable to evolving attack vectors, while contemporary deep neural networks operate as uninterpretable 'black boxes', failing regulatory audits mandated by international banking frameworks (such as Basel III and GDPR).")
    add_body("This project presents FraudShield, an explainable financial fraud intelligence platform engineered to demonstrate core Unit 2 Machine Learning classification principles. The system implements a multi-model architecture incorporating: (1) a manually derived linear discriminant function trained via closed-form ordinary least squares regression (w = (X^T X)^-1 X^T y); (2) a maximum-margin Linear Support Vector Machine (SVM) exposing hyperplane weights, bias, support vectors, and margin width (2 / ||w||); (3) a non-linear Radial Basis Function (RBF) Kernel SVM demonstrating the kernel trick on non-linearly separable fraud distributions; and (4) a probabilistic Logistic Regression baseline.")
    add_body("Rather than outputting opaque classifications, FraudShield provides full mathematical attribution by decomposing the discriminant score into exact per-feature contributions (w_i * x_i). Experimental evaluation on a standardized 6-feature transaction space and a non-linear concentric ring benchmark reveals that while Linear SVM fails on non-linear geometries (67.0% accuracy, 138 support vectors), the RBF Kernel model attains 100.0% accuracy (28 support vectors). Furthermore, the financial cost matrix is analyzed, highlighting why cyber-defense architectures must prioritize Recall over Precision to eradicate devastating False Negatives.")
    add_body("Keywords: Linear Discriminant Functions, Least-Squares Classification, Support Vector Machines, Margin Width, Kernel Trick, Radial Basis Function, Fraud Detection, Cost-Sensitive Learning.")

    doc.add_page_break()

    # ==========================================
    # 4. TABLE OF CONTENTS
    # ==========================================
    add_h1("TABLE OF CONTENTS")
    toc_items = [
        ("1. Introduction", "1"),
        ("    1.1 Background & Context", "1"),
        ("    1.2 The Problem of Black-Box Models in Financial Security", "2"),
        ("    1.3 Objectives of the Project", "2"),
        ("    1.4 Scope and Constraints", "3"),
        ("2. Theoretical Foundations & Mathematical Formulation", "4"),
        ("    2.1 Linear Discriminant Functions", "4"),
        ("    2.2 Parameter Estimation via Least-Squares Classification", "5"),
        ("    2.3 Maximum-Margin Hyperplanes & Linear SVM", "6"),
        ("    2.4 The Kernel Trick & Radial Basis Function (RBF) Kernels", "7"),
        ("    2.5 Probabilistic Modeling via Logistic Regression", "8"),
        ("3. System Design & Architectural Specification", "9"),
        ("    3.1 Multi-Tier Modular Architecture", "9"),
        ("    3.2 Feature Vector Design (R^6 Space)", "10"),
        ("    3.3 Database Schema & Audit Logging", "11"),
        ("    3.4 RESTful API & WebSocket Communication Specifications", "12"),
        ("4. Implementation Methodology", "13"),
        ("    4.1 Synthetic Data Generation & Z-Score Standardization", "13"),
        ("    4.2 Closed-Form Least-Squares Implementation", "14"),
        ("    4.3 Linear & Non-Linear SVM Implementation", "15"),
        ("    4.4 HTML5 Canvas Dynamic Decision Boundary Visualizer", "16"),
        ("5. Experimental Results, Analysis & Viva Discussion", "17"),
        ("    5.1 Model Evaluation Metrics on Banking Test Split", "17"),
        ("    5.2 Non-Linear Benchmark: Linear vs RBF Kernel Performance", "18"),
        ("    5.3 Feature Contribution Attribution & Explainability", "19"),
        ("    5.4 The Cost Asymmetry: False Negatives vs False Positives", "20"),
        ("6. Conclusion & Future Directions", "21"),
        ("References", "22"),
        ("Appendix: Key Mathematical Derivations & Code Extracts", "23")
    ]
    for title_toc, page_toc in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_after = Pt(2)
        r1 = p_toc.add_run(title_toc)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r2 = p_toc.add_run(f"  {'.' * (65 - len(title_toc))}  {page_toc}")
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(11)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 1: INTRODUCTION
    # ==========================================
    add_h1("CHAPTER 1: INTRODUCTION")
    add_h2("1.1 Background & Context")
    add_body("The digital transformation of the global financial sector has led to an exponential expansion in electronic payment processing, online banking transactions, and card-not-present (CNP) purchases. Concurrently, criminal fraud syndicates have evolved sophisticated countermeasures, resulting in billions of dollars in annual losses. Traditional financial security suites have historically relied upon hand-crafted heuristic rule engines (e.g., 'flag transaction if amount > $5000 and time is between 2:00 AM and 4:00 AM'). However, static heuristics exhibit high false-alarm rates and are incapable of detecting complex behavioral drifts or subtle cross-feature correlations.")

    add_h2("1.2 The Problem of Black-Box Models in Financial Security")
    add_body("While modern machine learning techniques offer significant pattern recognition capabilities, enterprise adoption in banking faces severe regulatory hurdles. In recent years, data science initiatives have frequently deployed Deep Neural Networks (DNNs), Random Forests, and XGBoost classifiers. While these architectures demonstrate high numerical accuracy, they act as uninterpretable black boxes. Regulatory bodies—including the Reserve Bank of India (RBI), the European Union General Data Protection Regulation (GDPR Article 22), and the Basel Committee on Banking Supervision—strictly mandate that financial institutions must be capable of providing explainable audit trails justifying why a customer's legitimate card was blocked or how a transaction was flagged as fraudulent.")

    add_h2("1.3 Objectives of the Project")
    add_body("The primary goal of FraudShield is to build an auditable, mathematically transparent classification system that bridges academic machine learning theory (specifically Unit 2: Linear Discriminants, SVMs, and Kernel Methods) with practical software engineering. The specific objectives include:")
    add_bullet("Implement a linear discriminant classifier from first principles using numpy, estimating parameters via the normal equations of least-squares classification.")
    add_bullet("Deconstruct the classification decision into individual feature contribution terms (w_i * x_i), enabling real-time visual explainability.")
    add_bullet("Expose the geometric internals of Support Vector Machines, including hyperplane weight vectors, intercept, support vector counts, and margin width.")
    add_bullet("Demonstrate the necessity of the Kernel Trick by visualizing decision boundaries on a non-linearly separable benchmark dataset.")
    add_bullet("Analyze the economic impact of classification errors, focusing on the cost asymmetry between False Negatives (missed fraud) and False Positives (customer friction).")

    add_h2("1.4 Scope and Constraints")
    add_body("To preserve academic rigor and maintain strict compliance with syllabus requirements, this project explicitly avoids deep learning, convolutional neural networks, transformers, large language models, random forests, and gradient boosting trees. All modeling is strictly confined to Unit 2 statistical classification theory.")

    # ==========================================
    # CHAPTER 2: THEORETICAL FOUNDATIONS
    # ==========================================
    add_h1("CHAPTER 2: THEORETICAL FOUNDATIONS & MATHEMATICAL FORMULATIONS")
    add_h2("2.1 Linear Discriminant Functions")
    add_body("A linear discriminant function is a linear combination of input features that partitions an input space R^d into distinct classification regions. For a binary classification setting where targets y in {0, 1}, the discriminant function is formally defined as:")
    add_code_block("g(x) = w^T x + b = sum_{i=1}^d (w_i * x_i) + b")
    add_body("Here, w = [w_1, w_2, ..., w_d]^T represents the weight vector (which defines the normal orientation of the separating hyperplane), x = [x_1, x_2, ..., x_d]^T is the feature vector, and b represents the scalar bias or threshold offset.")
    add_body("The decision rule classifies an input vector x into class 1 (Fraud) if g(x) >= 0.5 and class 0 (Legitimate) if g(x) < 0.5. A critical property of linear discriminants is feature additivity: each term w_i * x_i represents the signed scalar contribution of feature i toward the final verdict.")

    add_h2("2.2 Parameter Estimation via Least-Squares Classification")
    add_body("Linear classification can be viewed through the lens of ordinary regression. By augmenting the feature vector with a constant bias term x_aug = [x^T, 1]^T in R^{d+1}, we express the system as:")
    add_code_block("X_aug = [X, 1_N] in R^{N x (d+1)},    w_aug = [w^T, b]^T in R^{d+1}")
    add_body("The least-squares objective minimizes the sum of squared differences between continuous predictions and categorical target labels y in {0, 1}:")
    add_code_block("J(w_aug) = ||X_aug * w_aug - y||^2 = (X_aug * w_aug - y)^T (X_aug * w_aug - y)")
    add_body("Setting the gradient nabla_{w_aug} J = 0 yields the classic normal equations, solved using the Moore-Penrose pseudo-inverse:")
    add_code_block("w_aug = (X_aug^T X_aug)^-1 X_aug^T y")
    add_body("Viva Examination Note: While computationally efficient and closed-form, least-squares classification has a well-known vulnerability: outliers positioned deep within their correct class regions generate large squared error penalties, which can paradoxically rotate and displace the decision hyperplane away from optimal separation.")

    add_h2("2.3 Maximum-Margin Hyperplanes & Linear Support Vector Machines")
    add_body("To address the limitations of least-squares classification, Vapnik introduced Support Vector Machines (SVM). Rather than minimizing residual error across all samples, SVM identifies the optimal hyperplane that maximizes the geometric margin between classes.")
    add_body("The primal optimization problem for a linearly separable dataset is formulated as:")
    add_code_block("minimize_{w, b}  (1/2) * ||w||^2\nsubject to:      y_i * (w^T x_i + b) >= 1,   for all i = 1, ..., N")
    add_body("The geometric margin width M represents the perpendicular distance between the two supporting bounding planes (w^T x + b = +1 and w^T x + b = -1):")
    add_code_block("Margin Width (M) = 2 / ||w||_2")
    add_body("Data points x_i that satisfy y_i(w^T x_i + b) = 1 are termed Support Vectors. All other training samples have zero influence on the position of the separating plane. This property confers extreme structural robustness against non-boundary outliers.")

    add_h2("2.4 The Kernel Trick & Radial Basis Function (RBF) Kernels")
    add_body("When the true decision boundary is non-linear, no linear hyperplane in R^d can achieve acceptable separation without catastrophic misclassification. The Kernel Trick addresses this by implicitly projecting input vectors x into a higher- (or infinite-) dimensional Hilbert space H via a non-linear mapping Phi(x):")
    add_code_block("Phi: R^d -> H,    where  dim(H) >> d")
    add_body("By Mercer's Theorem, the inner product in H can be computed directly in the low-dimensional input space using a valid positive semi-definite kernel function K(x, x') = <Phi(x), Phi(x')>. FraudShield implements the Radial Basis Function (RBF) kernel:")
    add_code_block("K(x, x') = exp( -gamma * ||x - x'||^2 )")
    add_body("The parameter gamma = 1 / (2 * sigma^2) controls the radius of influence of each support vector. High values of gamma create localized, tightly-fitted boundaries, while low values produce smooth, generalized contours.")

    add_h2("2.5 Probabilistic Modeling via Logistic Regression")
    add_body("To complement geometric margin distances with calibrated posterior probabilities, FraudShield incorporates Logistic Regression as a baseline. The log-odds (logit) of fraud are modeled as a linear combination of features, mapped onto [0, 1] via the standard sigmoid function:")
    add_code_block("P(y = 1 | x) = sigma(w^T x + b) = 1 / (1 + exp(-(w^T x + b)))")

    # ==========================================
    # CHAPTER 3: SYSTEM ARCHITECTURE
    # ==========================================
    add_h1("CHAPTER 3: SYSTEM DESIGN & ARCHITECTURAL SPECIFICATION")
    add_h2("3.1 Multi-Tier Modular Architecture")
    add_body("FraudShield adheres to strict enterprise separation of concerns, structured into five decoupled layers:")
    add_bullet("Data Layer (/data_layer): Handles synthetic data generation, manual feature scaling, and CSV streaming.")
    add_bullet("Model Layer (/model_layer): Houses all mathematical classifier implementations, training pipelines, and 2D grid generation.")
    add_bullet("Storage Layer (/db): Manages SQLite persistence for audit logs and JWT user credential storage.")
    add_bullet("API Layer (/api_layer): Exposes asynchronous REST endpoints and WebSocket alert channels via FastAPI.")
    add_bullet("Presentation Layer (/frontend): Single-page dark-mode web application featuring real-time CSS charts and HTML5 Canvas boundary plots.")

    add_h2("3.2 Feature Vector Design (R^6 Space)")
    add_body("The primary transaction feature space consists of six continuous and categorical variables:")
    feats = [
        ("amount", "Continuous ($)", "Exponential tail. Normal purchases: $10–$500; Fraud purchases: $100–$10,000."),
        ("hour", "Discrete (0–23)", "Hour of day. Fraud peaks during late-night / off-peak hours (00:00–05:00)."),
        ("merchant_risk", "Continuous [0, 1]", "Vendor risk score sampled from Beta distribution: Beta(7,3) for fraud, Beta(2,8) for legitimate."),
        ("distance_from_home", "Continuous (km)", "Geographical distance from cardholder billing address. Exponentially higher for fraud."),
        ("transaction_velocity", "Integer (>= 1)", "Number of charges attempted in the preceding 60 minutes. Sampled via Poisson distribution."),
        ("is_international", "Binary {0, 1}", "Cross-border payment flag (60% occurrence in fraud vs 10% in normal transactions).")
    ]
    for fn, ftype, fdesc in feats:
        add_bullet(fdesc, bold_prefix=f"{fn} ({ftype}): ")

    add_h2("3.3 Database Schema & Audit Logging")
    add_body("The SQLite database (fraudshield.db) maintains an immutable audit ledger across two tables:")
    add_body("1. transactions Table: Stores unique transaction ID, ISO timestamp, 6 raw feature values, discriminant raw score, discriminant verdict, serialized JSON feature contributions, SVM decision score, SVM verdict, serialized JSON support vector details, and final fraud flag.")
    add_body("2. users Table: Manages administrative accounts with username, salt-hashed password (bcrypt), creation date, and last login timestamp.")

    add_h2("3.4 RESTful API & WebSocket Specifications")
    add_body("The FastAPI application exposes the following endpoints:")
    add_bullet("POST /api/predict: Consumes JSON feature payload, executes all 4 classifiers, logs to DB, broadcasts WebSocket alert if fraud, and returns full math breakdowns.")
    add_bullet("POST /api/batch: Accepts multipart/form-data CSV, processes transactions in a streaming loop, and returns bulk classifications with fraud summary counts.")
    add_bullet("GET /api/boundary?kernel=linear|rbf: Generates an 80x80 meshgrid over the 2D benchmark dataset, computing decision values Z for canvas heatmap rendering.")
    add_bullet("GET /api/metrics: Returns accuracy, precision, recall, F1, and full confusion matrices evaluated on the 20% stratified test split.")
    add_bullet("WebSocket /ws/alerts: Full-duplex WebSocket connection delivering instant push notifications to active dashboard sessions.")

    # ==========================================
    # CHAPTER 4: IMPLEMENTATION METHODOLOGY
    # ==========================================
    add_h1("CHAPTER 4: IMPLEMENTATION METHODOLOGY")
    add_h2("4.1 Synthetic Data Generation & Manual Z-Score Standardization")
    add_body("To eliminate artificial scaling bias, features are normalized using a custom FeatureScaler implemented in NumPy without scikit-learn dependencies. Means mu_j and standard deviations sigma_j are computed strictly on the training partition:")
    add_code_block("z_{ij} = (x_{ij} - mu_j) / (sigma_j + 1e-8)")

    add_h2("4.2 Closed-Form Least-Squares Implementation")
    add_body("The DiscriminantClassifier class performs augmentation and solves the normal equations using np.linalg.pinv to guarantee numerical stability even in the presence of collinearity:")
    add_code_block("X_aug = np.hstack([X, np.ones((X.shape[0], 1))])\nw_aug = np.linalg.pinv(X_aug.T @ X_aug) @ X_aug.T @ y\nself.weights = w_aug[:-1]\nself.bias = w_aug[-1]")

    add_h2("4.3 Linear & Non-Linear SVM Implementation")
    add_body("The LinearSVMClassifier and RBFSVMClassifier classes wrap scikit-learn's SVC primitives while exposing private attributes required for educational viva inspection: decision_function(), coef_, intercept_, and n_support_.")

    add_h2("4.4 HTML5 Canvas Dynamic Decision Boundary Visualizer")
    add_body("To demonstrate the kernel trick visually, ModelManager constructs a 200-sample concentric circular benchmark in R^2 (fraud points in an inner circle of radius r < 1.5, legitimate points in an outer ring of radius 2.5 < r < 4.0). The browser executes a bilinear contour traversal across an 80x80 decision grid Z, rendering the separating zero-level set (Z = 0) in amber gold alongside highlighted support vector markers.")

    # ==========================================
    # CHAPTER 5: EXPERIMENTAL RESULTS
    # ==========================================
    add_h1("CHAPTER 5: EXPERIMENTAL RESULTS, ANALYSIS & VIVA DISCUSSION")
    add_h2("5.1 Model Evaluation Metrics on Banking Test Split")
    add_body("The classifiers were evaluated on an 80/20 stratified train/test split (400 training samples, 100 test samples containing 80 legitimate and 20 fraud transactions). Table 5.1 details the empirical performance:")

    # Table 5.1
    t51 = doc.add_table(rows=5, cols=7)
    t51.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_headers = ["Model", "Accuracy", "Precision", "Recall", "F1-Score", "TN / FP", "FN / TP"]
    t_data = [
        ["Linear Discriminant", "99.0%", "100.0%", "95.0%", "97.4%", "80 / 0", "1 / 19"],
        ["Linear SVM", "99.0%", "100.0%", "95.0%", "97.4%", "80 / 0", "1 / 19"],
        ["RBF Kernel SVM", "100.0%", "100.0%", "100.0%", "100.0%", "80 / 0", "0 / 20"],
        ["Logistic Regression", "99.0%", "100.0%", "95.0%", "97.4%", "80 / 0", "1 / 19"]
    ]
    for c_idx, h in enumerate(t_headers):
        cell = t51.cell(0, c_idx)
        cell.text = h
        set_cell_background(cell, "1E3A8A")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(10)
    for r_idx, row_vals in enumerate(t_data):
        for c_idx, val in enumerate(row_vals):
            cell = t51.cell(r_idx + 1, c_idx)
            cell.text = val
            set_cell_background(cell, "F1F5F9" if r_idx % 2 == 0 else "FFFFFF")
            p = cell.paragraphs[0]
            p.runs[0].font.size = Pt(9.5)
            if r_idx == 2: # Highlight RBF
                p.runs[0].font.bold = True

    add_body("Table 5.1: Comparative classification metrics on held-out test split.", space_after=12)

    add_h2("5.2 Non-Linear Benchmark: Linear vs RBF Kernel Performance")
    add_body("When evaluated against the 2D concentric ring dataset, the fundamental limitation of linear classification becomes mathematically apparent:")
    add_bullet("Linear Kernel SVM: Attains only 67.0% Accuracy. Because a straight line cannot encapsulate a central cluster without bisecting the surrounding ring, 138 out of 200 data points (69%) are forced to become support vectors due to margin boundary violations.")
    add_bullet("RBF Kernel SVM: Attains 100.0% Accuracy. By projecting inputs into an infinite-dimensional RKHS, the model constructs a smooth, closed circular contour enclosing the fraud cluster, requiring only 28 support vectors (14%).")

    add_h2("5.3 Feature Contribution Attribution & Explainability")
    add_body("Analyzing the learned weights w across linear models reveals that merchant_risk (w = +1.4446) and distance_from_home (w = +0.6755) exert the strongest positive influence toward fraud verdicts, followed by amount (+0.6461) and transaction_velocity (+0.5700). In contrast, hour (-0.0493) exerts a mild negative bias during standard daytime hours, confirming intuitive banking logic.")

    add_h2("5.4 The Cost Asymmetry: False Negatives vs False Positives")
    add_body("In standard machine learning benchmarks, models are evaluated under symmetric zero-one loss. However, in financial cyber-defense, errors are profoundly asymmetric:")
    add_bullet("False Positive (FP): A legitimate purchase is flagged. The cardholder experiences slight friction (e.g., verifying identity via SMS OTP). Financial cost is negligible (approx. $25 in customer support overhead).")
    add_bullet("False Negative (FN): A fraudulent charge goes undetected. The fraudster completes the unauthorized transfer, resulting in direct balance depletion, interchange chargeback penalties, forensic investigation costs, and reputation damage (historically estimated at 3.0x the transaction amount).")
    add_body("Consequently, the optimal financial operating threshold must maximize Recall (Sensitivity = TP / (TP + FN)), accepting minor reductions in Precision to drive False Negatives strictly to zero.")

    # ==========================================
    # CHAPTER 6: CONCLUSION
    # ==========================================
    add_h1("CHAPTER 6: CONCLUSION & FUTURE DIRECTIONS")
    add_h2("6.1 Conclusion")
    add_body("FraudShield successfully operationalizes the theoretical constructs of Unit 2 Machine Learning into an auditable, enterprise-grade classification engine. By computing closed-form least-squares solutions, displaying maximum-margin support vector hyperplanes, and visually demonstrating kernel-induced non-linear separation on dynamic HTML5 canvases, the project establishes that explainable classical classification provides rigorous mathematical accountability that opaque deep-learning models cannot match.")

    add_h2("6.2 Future Work")
    add_body("Future enhancements planned for FraudShield include:")
    add_bullet("Streaming Pipeline Integration: Connecting the FastAPI backend to Apache Kafka and Redis for distributed sub-millisecond payment stream evaluation.")
    add_bullet("Kaggle European Dataset Ingestion: Validating the algorithms on the benchmark 284,807 European cardholder transaction dataset with PCA-transformed features.")
    add_bullet("Automated Grid Search & Cross-Validation: Implementing real-time hyperparameter tuning for SVM slack penalty C and RBF bandwidth gamma.")

    # ==========================================
    # REFERENCES
    # ==========================================
    add_h1("REFERENCES")
    refs = [
        "Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer, New York. (Chapter 4: Linear Models for Classification).",
        "Duda, R. O., Hart, P. E., & Stork, D. G. (2001). Pattern Classification (2nd ed.). John Wiley & Sons. (Chapter 5: Linear Discriminant Functions).",
        "Vapnik, V. (1998). Statistical Learning Theory. Wiley-Interscience, New York.",
        "Cortes, C., & Vapnik, V. (1995). Support-vector networks. Machine Learning, 20(3), 273-297.",
        "Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning: Data Mining, Inference, and Prediction (2nd ed.). Springer.",
        "Basel Committee on Banking Supervision. (2021). Sound Practices: Implications of fintech developments for banks and bank supervisors. Bank for International Settlements."
    ]
    for rf in refs:
        add_bullet(rf)

    output_path = os.path.join(os.getcwd(), "FraudShield_Project_Report.docx")
    doc.save(output_path)
    print(f"Project report successfully generated: {output_path}")

if __name__ == "__main__":
    create_report()
