import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # Theme Colors
    BG_DARK = RGBColor(15, 23, 42)       # Slate 900
    CARD_BG = RGBColor(30, 41, 59)       # Slate 800
    CARD_BORDER = RGBColor(51, 65, 85)   # Slate 700
    TEXT_LIGHT = RGBColor(248, 250, 252) # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184) # Slate 400
    ACCENT_CYAN = RGBColor(56, 189, 248) # Sky 400
    ACCENT_BLUE = RGBColor(59, 130, 246) # Blue 500
    COLOR_FRAUD = RGBColor(239, 68, 68)  # Red 500
    COLOR_SAFE = RGBColor(34, 197, 94)   # Green 500
    COLOR_WARN = RGBColor(245, 158, 11)  # Amber 500

    def add_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="FRAUDSHIELD • B.TECH CSE ML VIVA PROJECT"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    add_background(s1)

    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(2.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    
    p0 = tf1.paragraphs[0]
    p0.text = "MACHINE LEARNING COURSE PROJECT • UNIT 2"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_CYAN
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "FraudShield: Financial Fraud Intelligence"
    p1.font.size = Pt(38)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "Mathematical Classification with Discriminant Functions, Support Vector Machines & Kernel Methods"
    p2.font.size = Pt(18)
    p2.font.color.rgb = TEXT_MUTED

    # Meta card at bottom
    add_card(s1, Inches(1.0), Inches(4.7), Inches(11.333), Inches(1.8), bg_color=CARD_BG)
    meta_box = s1.shapes.add_textbox(Inches(1.3), Inches(4.9), Inches(10.7), Inches(1.4))
    tf_meta = meta_box.text_frame
    
    pm1 = tf_meta.paragraphs[0]
    pm1.text = "Candidate: 3rd Year B.Tech Computer Science & Engineering"
    pm1.font.size = Pt(15)
    pm1.font.bold = True
    pm1.font.color.rgb = TEXT_LIGHT
    pm1.space_after = Pt(6)

    pm2 = tf_meta.add_paragraph()
    pm2.text = "Key Focus Areas: Math Transparency • Manual Least Squares • Linear vs RBF Kernel Trick • High-Recall Cost Matrix"
    pm2.font.size = Pt(13)
    pm2.font.color.rgb = ACCENT_CYAN
    pm2.space_after = Pt(4)

    pm3 = tf_meta.add_paragraph()
    pm3.text = "Architecture: FastAPI Backend • Custom NumPy Algorithms • Scikit-Learn SVM • HTML5 Canvas Boundary Viz"
    pm3.font.size = Pt(12)
    pm3.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 2: Problem Statement & Motivation
    # ==========================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    add_background(s2)
    add_header(s2, "Problem Statement: Explainable Fraud Classification")

    # Left Card
    add_card(s2, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1))
    box2_l = s2.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.0), Inches(4.7))
    tf2_l = box2_l.text_frame
    tf2_l.word_wrap = True

    p = tf2_l.paragraphs[0]
    p.text = "The Modern Banking Challenge"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_FRAUD
    p.space_after = Pt(12)

    bullets_l = [
        "Card-Not-Present & cyber fraud cause billions in losses annually.",
        "Static Rule Engines fail to adapt to complex, multi-feature behavioral shifts.",
        "Black-Box ML (Deep Neural Nets) gives predictions without auditable mathematical reasoning.",
        "Regulatory standards (RBI, GDPR, Basel III) mandate accountability and explainable decision paths for denied transactions."
    ]
    for b in bullets_l:
        p = tf2_l.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(10)

    # Right Card
    add_card(s2, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1))
    box2_r = s2.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf2_r = box2_r.text_frame
    tf2_r.word_wrap = True

    p = tf2_r.paragraphs[0]
    p.text = "The FraudShield Objective"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_SAFE
    p.space_after = Pt(12)

    bullets_r = [
        "Unit 2 Concept Rigor: Implements linear discriminant functions from first mathematical principles.",
        "Hyperplane Transparency: Exposes exact weights, bias, support vectors, and margin widths.",
        "Kernel Trick Verification: Geometrically and numerically proves why non-linear fraud structures require RBF kernels.",
        "Asymmetric Cost Awareness: Models the real-world trade-off where False Negatives are far more dangerous than False Positives."
    ]
    for b in bullets_r:
        p = tf2_r.add_paragraph()
        p.text = "✔ " + b
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(10)

    # ==========================================
    # SLIDE 3: System Architecture & Feature Set
    # ==========================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    add_background(s3)
    add_header(s3, "Architecture & Feature Engineering Pipeline")

    # 3 Column Cards
    col_w = Inches(3.64)
    # Col 1: Data
    add_card(s3, Inches(0.8), Inches(1.7), col_w, Inches(5.1))
    b3_1 = s3.shapes.add_textbox(Inches(1.0), Inches(1.9), col_w - Inches(0.4), Inches(4.7))
    tf3_1 = b3_1.text_frame
    tf3_1.word_wrap = True
    p = tf3_1.paragraphs[0]
    p.text = "1. Data Layer"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(10)
    for txt in [
        "Synthetic Banking Generator: 500 samples (20% fraud, 80% legitimate) with realistic multi-modal distributions.",
        "Manual Z-Score Scaler: Implemented in pure NumPy: z = (x - μ) / σ to prevent feature scale distortion.",
        "CSV Batch Parser: Streaming CSV parser with validation for bulk audit uploads."
    ]:
        p = tf3_1.add_paragraph()
        p.text = "• " + txt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    # Col 2: Features
    add_card(s3, Inches(4.84), Inches(1.7), col_w, Inches(5.1))
    b3_2 = s3.shapes.add_textbox(Inches(5.04), Inches(1.9), col_w - Inches(0.4), Inches(4.7))
    tf3_2 = b3_2.text_frame
    tf3_2.word_wrap = True
    p = tf3_2.paragraphs[0]
    p.text = "2. 6-Feature Input Space"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(10)
    feats = [
        ("Amount ($)", "Exponential tail, fraud skew ($100-$10k)"),
        ("Hour of Day", "0-23h, fraud concentrated at late night"),
        ("Merchant Risk", "Beta(7,3) high risk vs Beta(2,8) normal"),
        ("Distance (km)", "Geo-deviation from cardholder home"),
        ("Velocity", "Charges in preceding 60 min (Poisson)"),
        ("International", "Binary indicator (0=domestic, 1=overseas)")
    ]
    for fn, fd in feats:
        p = tf3_2.add_paragraph()
        p.text = f"• {fn}: {fd}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(6)

    # Col 3: API & UI
    add_card(s3, Inches(8.88), Inches(1.7), col_w, Inches(5.1))
    b3_3 = s3.shapes.add_textbox(Inches(9.08), Inches(1.9), col_w - Inches(0.4), Inches(4.7))
    tf3_3 = b3_3.text_frame
    tf3_3.word_wrap = True
    p = tf3_3.paragraphs[0]
    p.text = "3. API & Web UI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(10)
    for txt in [
        "FastAPI Asynchronous Backend: Endpoints for /predict, /batch, /boundary, /metrics, and /history.",
        "SQLite Persistence: Stores transactions and full model decision breakdowns in fraudshield.db.",
        "WebSocket Push Engine: Real-time fraud alert delivery.",
        "Interactive HTML5 Canvas: Dynamic 2D decision boundary rendering."
    ]:
        p = tf3_3.add_paragraph()
        p.text = "• " + txt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    # ==========================================
    # SLIDE 4: Linear Discriminant Function
    # ==========================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    add_background(s4)
    add_header(s4, "Model 1: Linear Discriminant Function (Manual Least Squares)")

    add_card(s4, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1))
    b4_l = s4.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.0), Inches(4.7))
    tf4_l = b4_l.text_frame
    tf4_l.word_wrap = True
    p = tf4_l.paragraphs[0]
    p.text = "Mathematical Formulation"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(12)

    formula_items = [
        "Discriminant Function:",
        "    g(x) = wᵀx + b = w₁x₁ + w₂x₂ + ... + w₆x₆ + b",
        "Decision Boundary Criterion:",
        "    y_pred = 1 (FRAUD) if g(x) ≥ 0.5, else 0 (LEGIT)",
        "Least-Squares Weight Derivation (Normal Equation):",
        "    Augment matrix: X_aug = [X, 1]",
        "    w_aug = (X_augᵀ X_aug)⁻¹ X_augᵀ y",
        "    w = w_aug[:-1],   bias = w_aug[-1]",
        "Pure NumPy implementation with no scikit-learn dependency."
    ]
    for it in formula_items:
        p = tf4_l.add_paragraph()
        p.text = it
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(6)

    # Right Card: Viva Discussion
    add_card(s4, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1))
    b4_r = s4.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf4_r = b4_r.text_frame
    tf4_r.word_wrap = True
    p = tf4_r.paragraphs[0]
    p.text = "Explainability & Viva Insights"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_WARN
    p.space_after = Pt(12)

    viva_disc = [
        "Feature Attribution: The API returns the exact weighted contribution (w_i · x_i) for each feature rather than a single black-box score.",
        "Visual Risk Bars: The UI plots green (negative / safe) vs red (positive / risky) bars showing why a card was flagged.",
        "Least-Squares Sensitivity: In least-squares classification, points far into the safe region still produce errors, shifting the boundary. This demonstrates why SVM maximum margin is mathematically superior."
    ]
    for vd in viva_disc:
        p = tf4_r.add_paragraph()
        p.text = "• " + vd
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(10)

    # ==========================================
    # SLIDE 5: Linear Support Vector Machine
    # ==========================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    add_background(s5)
    add_header(s5, "Model 2: Linear Support Vector Machine (Maximum Margin)")

    add_card(s5, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1))
    b5_l = s5.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.0), Inches(4.7))
    tf5_l = b5_l.text_frame
    tf5_l.word_wrap = True
    p = tf5_l.paragraphs[0]
    p.text = "Primal Optimization & Geometry"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(12)

    svm_math = [
        "Objective: Maximize margin between classes:",
        "    min_{w,b}  (1/2) ||w||²",
        "    subject to: y_i (wᵀx_i + b) ≥ 1, ∀ i",
        "Margin Width Formulation:",
        "    Margin = 2 / ||w||₂",
        "Decision Function:",
        "    f(x) = wᵀx + b",
        "    Sign determines class (+1: Fraud, -1: Legit)",
        "    Magnitude measures distance from decision boundary."
    ]
    for sm in svm_math:
        p = tf5_l.add_paragraph()
        p.text = sm
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(7)

    add_card(s5, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1))
    b5_r = s5.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf5_r = b5_r.text_frame
    tf5_r.word_wrap = True
    p = tf5_r.paragraphs[0]
    p.text = "Live Model Introspection"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_SAFE
    p.space_after = Pt(12)

    svm_feats = [
        "Support Vector Extraction: Displays exact count of critical border samples (n_support_vectors).",
        "Margin Geometry Inspection: Real-time calculation and display of margin width (2 / ||w||).",
        "Learned Weight Vector:",
        "    • Merchant Risk: +1.44 (Strongest positive fraud predictor)",
        "    • Distance from Home: +0.68",
        "    • Transaction Amount: +0.65",
        "    • Velocity: +0.57",
        "    • Hour: -0.05 (Daytime slightly lowers baseline risk)"
    ]
    for sf in svm_feats:
        p = tf5_r.add_paragraph()
        p.text = sf
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(6)

    # ==========================================
    # SLIDE 6: The Kernel Trick (Non-Linear SVM)
    # ==========================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    add_background(s6)
    add_header(s6, "Model 3: The Kernel Trick & RBF Non-Linear Classification")

    add_card(s6, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1))
    b6_l = s6.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.0), Inches(4.7))
    tf6_l = b6_l.text_frame
    tf6_l.word_wrap = True
    p = tf6_l.paragraphs[0]
    p.text = "Why Do We Need Kernels?"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(12)

    kernel_pts = [
        "Real-world financial fraud is rarely linearly separable.",
        "Example: Coordinated fraud rings operating around common legitimate clusters create concentric or pocketed patterns.",
        "The Kernel Trick: Implicitly projects input x into an infinite-dimensional feature space Φ(x) without explicit mapping computation:",
        "    K(x, x') = ⟨Φ(x), Φ(x')⟩",
        "Radial Basis Function (RBF) Kernel:",
        "    K(x, x') = exp( -γ ||x - x'||² )",
        "Transforms complex geometric boundaries into linear separations in the dual Hilbert space."
    ]
    for kp in kernel_pts:
        p = tf6_l.add_paragraph()
        p.text = kp
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(6)

    # Right Card: The Concentric Benchmark Proof
    add_card(s6, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1))
    b6_r = s6.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf6_r = b6_r.text_frame
    tf6_r.word_wrap = True
    p = tf6_r.paragraphs[0]
    p.text = "Concentric Ring Benchmark (Live Experiment)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_WARN
    p.space_after = Pt(12)

    # Mini cards inside right section
    comp_items = [
        ("Linear Kernel SVM", "67.0% Accuracy", "138 / 200 Support Vectors", "A linear plane cuts across circles, misclassifying large clusters. Almost all points become support vectors.", COLOR_FRAUD),
        ("RBF Kernel SVM", "100.0% Accuracy", "28 / 200 Support Vectors", "RBF wraps an optimal circular boundary around the fraud cluster with a wide margin.", COLOR_SAFE)
    ]
    for title_k, acc_k, sv_k, desc_k, col_k in comp_items:
        p = tf6_r.add_paragraph()
        p.text = f"{title_k}  ➜  {acc_k}"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col_k
        p.space_after = Pt(2)
        p = tf6_r.add_paragraph()
        p.text = f"• Support Vectors: {sv_k}\n• {desc_k}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    # ==========================================
    # SLIDE 7: Model Comparison & Test Metrics Table
    # ==========================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    add_background(s7)
    add_header(s7, "Comprehensive Model Evaluation & Test Metrics")

    # Add Table
    rows = 5
    cols = 8
    t_left = Inches(0.8)
    t_top = Inches(1.7)
    t_width = Inches(11.733)
    t_height = Inches(3.0)
    table_shape = s7.shapes.add_table(rows, cols, t_left, t_top, t_width, t_height)
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(2.733)
    for c in range(1, cols):
        table.columns[c].width = Inches(1.285)

    headers = ["Model", "Accuracy", "Precision", "Recall", "F1-Score", "TN", "FP", "FN / TP"]
    data_rows = [
        ["Linear Discriminant", "99.0%", "100.0%", "95.0%", "97.4%", "80", "0", "1 / 19"],
        ["Linear SVM", "99.0%", "100.0%", "95.0%", "97.4%", "80", "0", "1 / 19"],
        ["RBF Kernel SVM", "100.0%", "100.0%", "100.0%", "100.0%", "80", "0", "0 / 20"],
        ["Logistic Regression", "99.0%", "100.0%", "95.0%", "97.4%", "80", "0", "1 / 19"]
    ]

    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(30, 58, 138) # Dark blue
        cell.text = h
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        p.alignment = PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT

    for i, row in enumerate(data_rows):
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if i % 2 == 0 else RGBColor(24, 33, 47)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(12)
            p.font.color.rgb = ACCENT_CYAN if (i == 2 and j == 0) else TEXT_LIGHT
            p.font.bold = (i == 2)
            p.alignment = PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT

    # Bottom Explanation Card
    add_card(s7, Inches(0.8), Inches(5.0), Inches(11.733), Inches(1.8), bg_color=CARD_BG)
    b7_bot = s7.shapes.add_textbox(Inches(1.1), Inches(5.1), Inches(11.1), Inches(1.6))
    tf7_bot = b7_bot.text_frame
    tf7_bot.word_wrap = True
    p = tf7_bot.paragraphs[0]
    p.text = "Key Viva Observation: The Cost Asymmetry of Financial Fraud"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_WARN
    p.space_after = Pt(4)

    for bullet in [
        "False Positive (FP): A legitimate purchase is flagged. User receives an SMS OTP (Minor friction cost ≈ $25).",
        "False Negative (FN): A fraudulent charge passes undetected. Direct financial loss + chargeback fines (≈ 3x charge amount).",
        "Conclusion: In financial cyber-defense, Recall (Sensitivity) is heavily prioritized over Precision to eliminate False Negatives."
    ]:
        p = tf7_bot.add_paragraph()
        p.text = "• " + bullet
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(2)

    # ==========================================
    # SLIDE 8: Interactive Web Application Demo
    # ==========================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    add_background(s8)
    add_header(s8, "FraudShield Interactive Web Application")

    # 4 Cards for 4 main features
    cw8 = Inches(2.7)
    spacing8 = Inches(0.24)
    lefts8 = [Inches(0.8) + i * (cw8 + spacing8) for i in range(4)]
    
    app_modules = [
        ("Single Transaction", "• Input 6 financial features\n• 1-Click Fraud / Legit sample fill\n• Real-time discriminant breakdown\n• Animated contribution bar chart\n• Decision threshold slider", ACCENT_CYAN),
        ("Kernel Visualizer", "• HTML5 600x600 Canvas plot\n• Concentric 2D ring dataset\n• Linear vs RBF toggle\n• Visual support vector markers\n• Boundary meshgrid contour", COLOR_SAFE),
        ("CSV Batch Processing", "• Bulk CSV drag-and-drop\n• Real-time row-by-row scoring\n• Multi-model verdict table\n• Fraud count summary cards\n• Auto-logs to SQLite audit DB", ACCENT_BLUE),
        ("Model Performance", "• Live test-set metrics\n• Side-by-side model cards\n• 2x2 confusion matrix grid\n• Precision / Recall / F1 tracking\n• Financial risk cost explanations", COLOR_WARN)
    ]

    for i, (m_title, m_desc, m_color) in enumerate(app_modules):
        add_card(s8, lefts8[i], Inches(1.7), cw8, Inches(5.1))
        b8 = s8.shapes.add_textbox(lefts8[i] + Inches(0.2), Inches(1.9), cw8 - Inches(0.4), Inches(4.7))
        tf8 = b8.text_frame
        tf8.word_wrap = True
        p = tf8.paragraphs[0]
        p.text = m_title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = m_color
        p.space_after = Pt(12)

        for line in m_desc.split("\n"):
            p = tf8.add_paragraph()
            p.text = line
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_LIGHT
            p.space_after = Pt(8)

    # ==========================================
    # SLIDE 9: Project File Structure
    # ==========================================
    s9 = prs.slides.add_slide(blank_slide_layout)
    add_background(s9)
    add_header(s9, "Project Architecture & Codebase Layout")

    add_card(s9, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1))
    b9_l = s9.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.0), Inches(4.7))
    tf9_l = b9_l.text_frame
    tf9_l.word_wrap = True
    p = tf9_l.paragraphs[0]
    p.text = "Directory Structure"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(10)

    tree = [
        "FraudShield/",
        "├── main.py                     (FastAPI Application & WebSockets)",
        "├── data_layer/",
        "│   ├── sample_data.py          (Synthetic Generator, 6 Features)",
        "│   ├── feature_engineering.py  (Manual Z-Score Scaler)",
        "│   └── csv_parser.py           (Batch Upload CSV Engine)",
        "├── model_layer/",
        "│   ├── discriminant.py         (Manual Least-Squares Classifier)",
        "│   ├── svm_models.py           (Linear & RBF Kernel SVM)",
        "│   ├── logistic_model.py       (Logistic Sigmoidal Classifier)",
        "│   └── model_manager.py        (Training & 2D Grid Coordinator)",
        "├── api_layer/                  (FastAPI Router Endpoints)",
        "├── db/                         (SQLite Audit Database & Auth)",
        "└── frontend/                   (HTML5, CSS3, Vanilla JS Dashboard)"
    ]
    for t in tree:
        p = tf9_l.add_paragraph()
        p.text = t
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(2)

    add_card(s9, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1))
    b9_r = s9.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf9_r = b9_r.text_frame
    tf9_r.word_wrap = True
    p = tf9_r.paragraphs[0]
    p.text = "Production-Ready Engineering"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_SAFE
    p.space_after = Pt(10)

    for eng in [
        "Separation of Concerns: Complete modular isolation between Data, Model, API, and UI layers.",
        "Zero Framework Bloat: Custom NumPy mathematical routines without heavy deep-learning dependencies.",
        "Database Persistence: All processed transactions stored in fraudshield.db with full score serializations.",
        "Real-Time Capabilities: WebSocket integration for live administrative fraud broadcast.",
        "REST API Compliance: Auto-generated OpenAPI / Swagger UI documentation at /docs."
    ]:
        p = tf9_r.add_paragraph()
        p.text = "✔ " + eng
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(10)

    # ==========================================
    # SLIDE 10: Conclusion & Academic Learnings
    # ==========================================
    s10 = prs.slides.add_slide(blank_slide_layout)
    add_background(s10)
    add_header(s10, "Summary, Academic Learnings & Future Scope")

    add_card(s10, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1))
    b10_l = s10.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.0), Inches(4.7))
    tf10_l = b10_l.text_frame
    tf10_l.word_wrap = True
    p = tf10_l.paragraphs[0]
    p.text = "Key Academic Learnings"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(12)

    learnings = [
        "Linear Discriminants via Least-Squares: Proved how ordinary regression acts as a linear classifier and mathematically observed boundary shifting caused by outliers.",
        "Margin Maximization: Understood why maximizing 2/||w|| produces superior generalization compared to minimizing total squared residuals.",
        "The Kernel Trick: Directly witnessed how transforming non-linear clusters into higher-dimensional representations enables 100% linear separability.",
        "Cost-Sensitive Classification: Recognized that in fraud detection, optimizing for accuracy alone is dangerous without evaluating False Negatives."
    ]
    for l in learnings:
        p = tf10_l.add_paragraph()
        p.text = "• " + l
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    add_card(s10, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1))
    b10_r = s10.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf10_r = b10_r.text_frame
    tf10_r.word_wrap = True
    p = tf10_r.paragraphs[0]
    p.text = "Future Scope"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_WARN
    p.space_after = Pt(12)

    future = [
        "Automated Hyperparameter Grid Search: Online tuning of SVM slack parameter C and RBF kernel parameter γ.",
        "Streaming Big Data Ingestion: Connecting the API layer to Apache Kafka for sub-millisecond fraud scoring on live card terminal streams.",
        "Public Benchmark Integration: Ingesting the real-world Kaggle European Cardholders 284,000 transaction dataset (with PCA features).",
        "Adaptive Concept Drift Retraining: Dynamically shifting decision hyperplanes when consumer spending patterns change during holiday seasons."
    ]
    for f in future:
        p = tf10_r.add_paragraph()
        p.text = "➜ " + f
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    # ==========================================
    # SLIDE 11: Viva Q&A Cheat Sheet
    # ==========================================
    s11 = prs.slides.add_slide(blank_slide_layout)
    add_background(s11)
    add_header(s11, "Viva Voce Reference & Examiner Q&A Guide")

    # 3 horizontal cards
    ch11 = Inches(1.5)
    qa_list = [
        ("Q1: Why does Least Squares work as a classifier, and what is its main drawback?",
         "A: By assigning targets {0, 1}, least-squares solves w = (XᵀX)⁻¹Xᵀy to minimize MSE. Its drawback is sensitivity to outliers: points correctly classified far from the boundary still generate large squared errors, which unfairly pulls the decision plane.",
         Inches(1.7)),
        ("Q2: What is the physical and mathematical meaning of margin width 2 / ||w||?",
         "A: It represents the orthogonal distance between the positive and negative supporting hyperplanes (wᵀx + b = +1 and wᵀx + b = -1). Maximizing this margin minimizes the VC dimension, improving generalization on unseen test data.",
         Inches(3.45)),
        ("Q3: Why did Linear SVM require 138 Support Vectors, while RBF SVM only needed 28?",
         "A: In the concentric ring dataset, a linear line cannot separate inner fraud from outer legitimate points. Almost all points near the center violate the margin constraint and become support vectors. The RBF kernel maps data to a space where a clean circular contour separates classes with only 28 boundary points.",
         Inches(5.2))
    ]

    for q_title, q_ans, top_pos in qa_list:
        add_card(s11, Inches(0.8), top_pos, Inches(11.733), ch11)
        b11 = s11.shapes.add_textbox(Inches(1.1), top_pos + Inches(0.12), Inches(11.1), ch11 - Inches(0.24))
        tf11 = b11.text_frame
        tf11.word_wrap = True
        p = tf11.paragraphs[0]
        p.text = q_title
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN
        p.space_after = Pt(4)
        p = tf11.add_paragraph()
        p.text = q_ans
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT

    # Save presentation
    output_path = os.path.join(os.getcwd(), "FraudShield_Presentation.pptx")
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_presentation()
