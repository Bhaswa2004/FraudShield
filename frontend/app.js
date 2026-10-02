document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const form = document.getElementById('transaction-form');
    const btnSampleLegit = document.getElementById('btn-sample-legit');
    const btnSampleFraud = document.getElementById('btn-sample-fraud');
    const resultsPanel = document.getElementById('results-panel');
    
    // Event Listeners
    btnSampleLegit.addEventListener('click', fillSampleLegit);
    btnSampleFraud.addEventListener('click', fillSampleFraud);
    form.addEventListener('submit', handleFormSubmit);

    // Tab navigation
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });
    
    // Batch upload
    document.getElementById('btn-upload').addEventListener('click', () => {
        document.getElementById('csv-file').click();
    });
    document.getElementById('csv-file').addEventListener('change', handleFileSelect);
    document.getElementById('btn-process').addEventListener('click', processBatch);
    document.getElementById('btn-sample-csv').addEventListener('click', downloadSampleCSV);
    
    // Kernel viz
    document.getElementById('btn-kernel-linear').addEventListener('click', () => loadBoundary('linear'));
    document.getElementById('btn-kernel-rbf').addEventListener('click', () => loadBoundary('rbf'));

    // Feature importance tabs
    document.querySelectorAll('.imp-tab').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.imp-tab').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderImportanceModel(btn.dataset.model);
        });
    });
    
    // Retrain
    const btnRetrainUpload = document.getElementById('btn-retrain-upload');
    if (btnRetrainUpload) {
        btnRetrainUpload.addEventListener('click', () => document.getElementById('retrain-file').click());
        document.getElementById('retrain-file').addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                document.getElementById('retrain-file-name').textContent = file.name;
                document.getElementById('btn-retrain').disabled = false;
            }
        });
        document.getElementById('btn-retrain').addEventListener('click', retrainModels);
        document.getElementById('btn-sample-train-csv').addEventListener('click', downloadSampleTrainingCSV);
    }
    
    // Auth
    const authForm = document.getElementById('auth-form');
    if (authForm) {
        authForm.addEventListener('submit', handleAuth);
        document.getElementById('auth-switch').addEventListener('click', toggleAuthMode);
        document.getElementById('auth-skip').addEventListener('click', () => {
            document.getElementById('auth-overlay').classList.add('hidden');
        });
    }
    const btnLogin = document.getElementById('btn-login');
    if (btnLogin) {
        btnLogin.addEventListener('click', () => document.getElementById('auth-overlay').classList.remove('hidden'));
    }
    const btnLogout = document.getElementById('btn-logout');
    if (btnLogout) {
        btnLogout.addEventListener('click', logout);
    }
    
    // Check existing auth & connect WebSocket
    checkAuth();
    connectAlertWebSocket();

    // Initial data load
    loadHistory();
});

function fillSampleLegit() {
    document.getElementById('amount').value = 45;
    document.getElementById('hour').value = 14;
    document.getElementById('merchant_risk').value = 0.15;
    document.getElementById('distance_from_home').value = 5;
    document.getElementById('transaction_velocity').value = 1;
    document.getElementById('is_international').value = 0;
}

function fillSampleFraud() {
    document.getElementById('amount').value = 2500;
    document.getElementById('hour').value = 2;
    document.getElementById('merchant_risk').value = 0.85;
    document.getElementById('distance_from_home').value = 150;
    document.getElementById('transaction_velocity').value = 7;
    document.getElementById('is_international').value = 1;
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const submitBtn = document.querySelector('#transaction-form button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Analyzing...';
    submitBtn.disabled = true;

    const payload = {
        amount: parseFloat(document.getElementById('amount').value),
        hour: parseInt(document.getElementById('hour').value),
        merchant_risk: parseFloat(document.getElementById('merchant_risk').value),
        distance_from_home: parseFloat(document.getElementById('distance_from_home').value),
        transaction_velocity: parseInt(document.getElementById('transaction_velocity').value),
        is_international: parseInt(document.getElementById('is_international').value)
    };

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        renderResults(data);
        await loadHistory();
    } catch (error) {
        console.error('Prediction failed:', error);
        alert('Failed to analyze transaction: ' + error.message);
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

function renderResults(data) {
    // 1. Verdict Banner
    const banner = document.getElementById('verdict-banner');
    const verdictText = document.getElementById('verdict-text');
    const icon = document.getElementById('verdict-icon');
    
    banner.className = 'verdict-banner ' + (data.is_fraud_predicted ? 'fraud' : 'legit');
    verdictText.textContent = data.is_fraud_predicted ? 'FRAUD DETECTED' : 'LEGITIMATE';
    icon.innerHTML = data.is_fraud_predicted ? '⚠️' : '✅';

    // 2. Model Comparison Table - now 4 models
    const tbody = document.getElementById('comparison-tbody');
    tbody.innerHTML = `
        <tr>
            <td>Discriminant Function</td>
            <td class="mono">${data.discriminant.raw_score.toFixed(4)}</td>
            <td><span class="badge ${data.discriminant.verdict === 'FRAUD' ? 'fraud' : 'legit'}">${data.discriminant.verdict}</span></td>
            <td>${(data.discriminant.confidence * 100).toFixed(1)}%</td>
        </tr>
        <tr>
            <td>Linear SVM</td>
            <td class="mono">${data.svm.decision_value.toFixed(4)}</td>
            <td><span class="badge ${data.svm.verdict === 'FRAUD' ? 'fraud' : 'legit'}">${data.svm.verdict}</span></td>
            <td>${(data.svm.confidence * 100).toFixed(1)}%</td>
        </tr>
        <tr>
            <td>RBF SVM</td>
            <td class="mono">${data.rbf_svm.decision_value.toFixed(4)}</td>
            <td><span class="badge ${data.rbf_svm.verdict === 'FRAUD' ? 'fraud' : 'legit'}">${data.rbf_svm.verdict}</span></td>
            <td>${(data.rbf_svm.confidence * 100).toFixed(1)}%</td>
        </tr>
        <tr>
            <td>Logistic Regression</td>
            <td class="mono">${data.logistic.probability_fraud.toFixed(4)}</td>
            <td><span class="badge ${data.logistic.verdict === 'FRAUD' ? 'fraud' : 'legit'}">${data.logistic.verdict}</span></td>
            <td>${(data.logistic.confidence * 100).toFixed(1)}%</td>
        </tr>
    `;

    // 3. Discriminant Details
    document.getElementById('discriminant-raw').textContent = data.discriminant.raw_score.toFixed(4);
    document.getElementById('discriminant-threshold').textContent = data.discriminant.threshold.toFixed(4);
    document.getElementById('discriminant-bias').textContent = data.discriminant.bias.toFixed(4);
    renderContributionBars(data.discriminant.weighted_terms);
    renderScoreLine(data.discriminant.raw_score, data.discriminant.threshold, 'discriminant-number-line', true);

    // 4. SVM Details
    document.getElementById('svm-decision').textContent = data.svm.decision_value.toFixed(4);
    document.getElementById('svm-margin').textContent = data.svm.margin_width.toFixed(4);
    document.getElementById('svm-sv-counts').textContent = `[${data.svm.n_support_vectors.join(', ')}]`;
    
    const weightsTbody = document.getElementById('svm-weights-tbody');
    weightsTbody.innerHTML = '';
    for (const [feature, weight] of Object.entries(data.svm.weight_vector)) {
        weightsTbody.innerHTML += `
            <tr>
                <td>${formatFeatureName(feature)}</td>
                <td class="mono">${weight.toFixed(4)}</td>
            </tr>
        `;
    }
    // SVM threshold is typically 0
    renderScoreLine(data.svm.decision_value, 0, 'svm-number-line', false);

    // Show panel
    const resultsPanel = document.getElementById('results-panel');
    resultsPanel.classList.remove('hidden');
    resultsPanel.scrollIntoView({ behavior: 'smooth' });
}

function formatFeatureName(name) {
    const map = {
        'amount': 'Transaction Amount',
        'hour': 'Hour of Day',
        'merchant_risk': 'Merchant Risk',
        'distance_from_home': 'Distance from Home',
        'transaction_velocity': 'Transaction Velocity',
        'is_international': 'International'
    };
    return map[name] || name;
}

function renderContributionBars(terms) {
    const container = document.getElementById('contribution-bars');
    container.innerHTML = '';
    
    // Find max absolute contribution for scaling
    let maxAbs = 0;
    for (const term of Object.values(terms)) {
        if (Math.abs(term.contribution) > maxAbs) {
            maxAbs = Math.abs(term.contribution);
        }
    }
    
    // Ensure we don't divide by 0
    maxAbs = maxAbs || 1;

    for (const [feature, details] of Object.entries(terms)) {
        const val = details.contribution;
        const percent = (Math.abs(val) / maxAbs) * 100;
        const isPositive = val >= 0;
        
        container.innerHTML += `
            <div class="bar-row">
                <div class="bar-label" title="${formatFeatureName(feature)}">${formatFeatureName(feature)}</div>
                <div class="bar-track">
                    <div class="bar-center"></div>
                    <div class="contribution-bar ${isPositive ? 'positive' : 'negative'}" style="width: 0%" data-target-width="${percent}%"></div>
                </div>
                <div class="bar-value ${isPositive ? 'text-danger' : 'text-safe'}">${val > 0 ? '+' : ''}${val.toFixed(4)}</div>
            </div>
        `;
    }

    // Trigger animation
    setTimeout(() => {
        document.querySelectorAll('.contribution-bar').forEach(bar => {
            bar.style.width = bar.getAttribute('data-target-width');
        });
    }, 50);
}

function renderScoreLine(score, threshold, containerId, isDiscriminant) {
    const container = document.getElementById(containerId);
    
    // Calculate a reasonable range to display based on the score and threshold
    let min, max;
    if (isDiscriminant) {
        // typically discriminant scores might be around threshold +/- a few units
        const diff = Math.max(Math.abs(score - threshold) * 2, 5);
        min = threshold - diff;
        max = threshold + diff;
    } else {
        // SVM decision values
        const diff = Math.max(Math.abs(score) * 2, 2);
        min = -diff;
        max = diff;
    }

    // Clamp percentage between 5% and 95% for visual reasons
    let percent = ((score - min) / (max - min)) * 100;
    percent = Math.max(5, Math.min(95, percent));
    
    const threshPercent = ((threshold - min) / (max - min)) * 100;

    const isDanger = score > threshold;

    container.innerHTML = `
        <div class="nl-axis"></div>
        <div class="nl-threshold" style="left: ${threshPercent}%"></div>
        <div class="nl-marker ${isDanger ? 'danger' : ''}" style="left: ${percent}%" title="Score: ${score.toFixed(4)}"></div>
    `;
}

async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        if (!response.ok) return;
        const data = await response.json();
        
        const tbody = document.getElementById('history-tbody');
        const alertsContainer = document.getElementById('alerts-container');
        
        tbody.innerHTML = '';
        alertsContainer.innerHTML = '';

        const transactions = data.transactions || [];
        
        transactions.forEach(tx => {
            // History Table Row
            const isFraud = tx.is_fraud_predicted;
            tbody.innerHTML += `
                <tr class="${isFraud ? 'row-fraud' : ''}">
                    <td>#${tx.id || tx.transaction_id || '?'}</td>
                    <td>${formatTimestamp(tx.timestamp)}</td>
                    <td>$${parseFloat(tx.amount).toFixed(2)}</td>
                    <td class="mono">${parseFloat(tx.discriminant_score).toFixed(4)}</td>
                    <td class="mono">${parseFloat(tx.svm_score).toFixed(4)}</td>
                    <td><span class="badge ${isFraud ? 'fraud' : 'legit'}">${isFraud ? 'FRAUD' : 'LEGIT'}</span></td>
                </tr>
            `;

            // Alert Card
            if (isFraud) {
                alertsContainer.innerHTML += `
                    <div class="alert-card">
                        <div class="alert-card-header">
                            ⚠️ Fraud Alert - TX #${tx.id || tx.transaction_id || '?'}
                        </div>
                        <div class="alert-details">
                            Time: ${formatTimestamp(tx.timestamp)} <br>
                            Amount: $${parseFloat(tx.amount).toFixed(2)} | Velocity: ${tx.transaction_velocity}
                        </div>
                    </div>
                `;
            }
        });
        
        if (transactions.filter(tx => tx.is_fraud_predicted).length === 0) {
            alertsContainer.innerHTML = '<p style="color: var(--text-secondary); font-size: 0.875rem;">No fraud alerts detected.</p>';
        }

    } catch (e) {
        console.error("Failed to load history", e);
    }
}

function formatTimestamp(isoStr) {
    if (!isoStr) return 'N/A';
    const date = new Date(isoStr);
    return date.toLocaleString();
}

function switchTab(tabId) {
    // Hide all tab sections
    ['single-section', 'batch-section', 'kernel-section', 'metrics-section', 'importance-section', 'retrain-section', 'roi-section'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.add('hidden');
    });
    
    // Deactivate all tabs
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    
    // Show selected section
    const section = document.getElementById(tabId);
    if (section) section.classList.remove('hidden');
    
    // Activate selected tab
    const tabBtn = document.querySelector(`[data-tab="${tabId}"]`);
    if (tabBtn) tabBtn.classList.add('active');
    
    // Load data for certain tabs
    if (tabId === 'kernel-section') {
        loadBoundary('linear');
    } else if (tabId === 'metrics-section') {
        loadMetrics();
    } else if (tabId === 'importance-section') {
        loadFeatureImportance();
    } else if (tabId === 'roi-section') {
        loadROI();
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        document.getElementById('file-name').textContent = file.name;
        document.getElementById('btn-process').disabled = false;
    }
}

function downloadSampleCSV() {
    const csv = `amount,hour,merchant_risk,distance_from_home,transaction_velocity,is_international
45.00,14,0.15,5.0,1,0
2500.00,2,0.85,150.0,7,1
120.00,10,0.25,12.0,2,0
800.00,3,0.70,80.0,5,1
35.00,16,0.10,3.0,1,0
3200.00,1,0.90,200.0,8,1
67.50,11,0.20,8.5,1,0
950.00,23,0.65,95.0,6,1
28.00,15,0.12,4.0,1,0
1800.00,4,0.78,120.0,4,1`;
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'sample_transactions.csv';
    a.click();
    URL.revokeObjectURL(url);
}

async function processBatch() {
    const file = document.getElementById('csv-file').files[0];
    if (!file) return;
    
    const btn = document.getElementById('btn-process');
    btn.textContent = 'Processing...';
    btn.disabled = true;
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/batch', {
            method: 'POST',
            body: formData
        });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Batch processing failed');
        }
        const data = await response.json();
        renderBatchResults(data);
    } catch (error) {
        alert('Batch error: ' + error.message);
    } finally {
        btn.textContent = 'Process Batch';
        btn.disabled = false;
    }
}

function renderBatchResults(data) {
    const summaryEl = document.getElementById('batch-summary');
    summaryEl.innerHTML = `
        <div class="batch-stat">
            <div class="stat-value">${data.total}</div>
            <div class="stat-label">Total</div>
        </div>
        <div class="batch-stat">
            <div class="stat-value text-danger">${data.fraud_count}</div>
            <div class="stat-label">Fraud</div>
        </div>
        <div class="batch-stat">
            <div class="stat-value text-safe">${data.legit_count}</div>
            <div class="stat-label">Legitimate</div>
        </div>
    `;
    
    const tbody = document.getElementById('batch-tbody');
    tbody.innerHTML = '';
    data.results.forEach(r => {
        const isFraud = r.is_fraud_predicted;
        tbody.innerHTML += `
            <tr class="${isFraud ? 'row-fraud' : ''}">
                <td>${r.row}</td>
                <td>$${r.features.amount.toFixed(2)}</td>
                <td class="mono">${r.discriminant.raw_score.toFixed(4)}</td>
                <td class="mono">${r.svm.decision_value.toFixed(4)}</td>
                <td class="mono">${r.rbf_svm.decision_value.toFixed(4)}</td>
                <td class="mono">${(r.logistic.probability_fraud * 100).toFixed(1)}%</td>
                <td><span class="badge ${isFraud ? 'fraud' : 'legit'}">${isFraud ? 'FRAUD' : 'LEGIT'}</span></td>
            </tr>
        `;
    });
    
    document.getElementById('batch-results').classList.remove('hidden');
    loadHistory();
}

async function loadBoundary(kernel) {
    // Update button states
    document.getElementById('btn-kernel-linear').classList.toggle('active', kernel === 'linear');
    document.getElementById('btn-kernel-rbf').classList.toggle('active', kernel === 'rbf');
    
    try {
        const response = await fetch(`/api/boundary?kernel=${kernel}`);
        if (!response.ok) throw new Error('Failed to load boundary data');
        const data = await response.json();
        
        document.getElementById('kernel-accuracy').textContent = `Accuracy: ${(data.accuracy * 100).toFixed(1)}%`;
        drawBoundary(data);
    } catch (error) {
        console.error('Boundary load error:', error);
    }
}

function drawBoundary(data) {
    const canvas = document.getElementById('boundary-canvas');
    const ctx = canvas.getContext('2d');
    const W = canvas.width;
    const H = canvas.height;
    const pad = 40;  // padding
    const plotW = W - 2 * pad;
    const plotH = H - 2 * pad;
    
    ctx.clearRect(0, 0, W, H);
    
    const { x_min, x_max, y_min, y_max, resolution, z_values } = data.grid;
    
    // Map data coords to canvas coords
    function toCanvasX(x) { return pad + ((x - x_min) / (x_max - x_min)) * plotW; }
    function toCanvasY(y) { return pad + ((y_max - y) / (y_max - y_min)) * plotH; }  // flip Y
    
    // Draw decision boundary heatmap
    const cellW = plotW / resolution;
    const cellH = plotH / resolution;
    
    for (let i = 0; i < resolution; i++) {
        for (let j = 0; j < resolution; j++) {
            const z = z_values[i][j];
            // Map z to color: negative (blue/legit region), positive (red/fraud region)
            let r, g, b, alpha;
            if (z > 0) {
                // Fraud region - red tones
                const intensity = Math.min(Math.abs(z) / 2, 1);
                r = 239; g = 68; b = 68;
                alpha = 0.1 + intensity * 0.3;
            } else {
                // Legit region - blue tones
                const intensity = Math.min(Math.abs(z) / 2, 1);
                r = 59; g = 130; b = 246;
                alpha = 0.1 + intensity * 0.3;
            }
            ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${alpha})`;
            ctx.fillRect(pad + j * cellW, pad + i * cellH, cellW + 0.5, cellH + 0.5);
        }
    }
    
    // Draw decision boundary contour (z ≈ 0)
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 2;
    for (let i = 0; i < resolution - 1; i++) {
        for (let j = 0; j < resolution - 1; j++) {
            const z00 = z_values[i][j];
            const z01 = z_values[i][j+1];
            const z10 = z_values[i+1][j];
            // If sign changes between adjacent cells, draw a boundary segment
            if ((z00 * z01 < 0) || (z00 * z10 < 0)) {
                const cx = pad + (j + 0.5) * cellW;
                const cy = pad + (i + 0.5) * cellH;
                ctx.fillStyle = '#f59e0b';
                ctx.fillRect(cx - 1, cy - 1, 2, 2);
            }
        }
    }
    
    // Draw support vectors (larger, outlined)
    data.support_vectors.forEach(sv => {
        const cx = toCanvasX(sv[0]);
        const cy = toCanvasY(sv[1]);
        ctx.beginPath();
        ctx.arc(cx, cy, 8, 0, 2 * Math.PI);
        ctx.strokeStyle = '#f59e0b';
        ctx.lineWidth = 2;
        ctx.stroke();
    });
    
    // Draw training points
    const points = data.points;
    for (let i = 0; i < points.X.length; i++) {
        const cx = toCanvasX(points.X[i][0]);
        const cy = toCanvasY(points.X[i][1]);
        const isFraud = points.y[i] === 1;
        
        ctx.beginPath();
        ctx.arc(cx, cy, 4, 0, 2 * Math.PI);
        ctx.fillStyle = isFraud ? '#ef4444' : '#3b82f6';
        ctx.fill();
        ctx.strokeStyle = 'rgba(255,255,255,0.5)';
        ctx.lineWidth = 1;
        ctx.stroke();
    }
    
    // Draw axes labels
    ctx.fillStyle = '#94a3b8';
    ctx.font = '12px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText('Feature 1', W / 2, H - 8);
    ctx.save();
    ctx.translate(12, H / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('Feature 2', 0, 0);
    ctx.restore();
    
    // Draw title
    ctx.fillStyle = '#e2e8f0';
    ctx.font = 'bold 14px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText(`Decision Boundary — ${data.kernel.toUpperCase()} Kernel`, W / 2, 20);
}

async function loadMetrics() {
    try {
        const response = await fetch('/api/metrics');
        if (!response.ok) throw new Error('Failed to load metrics');
        const data = await response.json();
        renderMetrics(data);
    } catch (error) {
        console.error('Metrics load error:', error);
    }
}

function renderMetrics(data) {
    const grid = document.getElementById('metrics-grid');
    grid.innerHTML = '';
    
    const modelNames = {
        'discriminant': 'Discriminant Function',
        'linear_svm': 'Linear SVM',
        'rbf_svm': 'RBF SVM',
        'logistic': 'Logistic Regression'
    };
    
    for (const [key, name] of Object.entries(modelNames)) {
        const m = data[key];
        if (!m) continue;
        const cm = m.confusion_matrix; // [[TN, FP], [FN, TP]]
        
        grid.innerHTML += `
            <div class="metric-card">
                <h4>${name}</h4>
                <div class="metric-row">
                    <span class="metric-label">Accuracy</span>
                    <span class="metric-value">${(m.accuracy * 100).toFixed(1)}%</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Precision</span>
                    <span class="metric-value">${(m.precision * 100).toFixed(1)}%</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Recall</span>
                    <span class="metric-value">${(m.recall * 100).toFixed(1)}%</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">F1 Score</span>
                    <span class="metric-value">${(m.f1 * 100).toFixed(1)}%</span>
                </div>
                <div class="confusion-matrix">
                    <div class="cm-header"></div>
                    <div class="cm-header">Pred Legit</div>
                    <div class="cm-header">Pred Fraud</div>
                    <div class="cm-header">Actual Legit</div>
                    <div class="cm-cell cm-tn">${cm[0][0]}</div>
                    <div class="cm-cell cm-fp">${cm[0][1]}</div>
                    <div class="cm-header">Actual Fraud</div>
                    <div class="cm-cell cm-fn">${cm[1][0]}</div>
                    <div class="cm-cell cm-tp">${cm[1][1]}</div>
                </div>
            </div>
        `;
    }
    
    // Note about FN vs FP
    if (data.note) {
        document.getElementById('metrics-note').innerHTML = `
            <strong>⚠️ Why False Negatives Matter More:</strong><br>
            ${data.note}
        `;
    }
    }
}

// ========== AUTH ==========
let authMode = 'login';
let authToken = localStorage.getItem('fraudshield_token');

function toggleAuthMode(e) {
    e.preventDefault();
    authMode = authMode === 'login' ? 'register' : 'login';
    document.getElementById('auth-title').textContent = authMode === 'login' ? 'Login to FraudShield' : 'Register for FraudShield';
    document.querySelector('#auth-form button[type="submit"]').textContent = authMode === 'login' ? 'Login' : 'Register';
    const toggleP = document.querySelector('.auth-toggle');
    if (toggleP) {
        toggleP.innerHTML = authMode === 'login'
            ? 'Don\'t have an account? <a href="#" id="auth-switch">Register</a>'
            : 'Already have an account? <a href="#" id="auth-switch">Login</a>';
        document.getElementById('auth-switch').addEventListener('click', toggleAuthMode);
    }
    const errEl = document.getElementById('auth-error');
    if (errEl) errEl.classList.add('hidden');
}

async function handleAuth(e) {
    e.preventDefault();
    const username = document.getElementById('auth-username').value;
    const password = document.getElementById('auth-password').value;
    const errorEl = document.getElementById('auth-error');

    try {
        const endpoint = authMode === 'login' ? '/api/auth/login' : '/api/auth/register';
        const resp = await fetch(endpoint, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'Authentication failed');

        if (authMode === 'register') {
            const loginResp = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, password})
            });
            const loginData = await loginResp.json();
            if (!loginResp.ok) throw new Error(loginData.detail);
            authToken = loginData.token;
        } else {
            authToken = data.token;
        }

        localStorage.setItem('fraudshield_token', authToken);
        document.getElementById('auth-overlay').classList.add('hidden');
        updateUserUI(username);
    } catch (err) {
        if (errorEl) {
            errorEl.textContent = err.message;
            errorEl.classList.remove('hidden');
        }
    }
}

async function checkAuth() {
    if (!authToken) return;
    try {
        const resp = await fetch('/api/auth/me', {
            headers: {'Authorization': `Bearer ${authToken}`}
        });
        if (resp.ok) {
            const data = await resp.json();
            updateUserUI(data.username);
        } else {
            localStorage.removeItem('fraudshield_token');
            authToken = null;
        }
    } catch (e) {
        console.error('Auth check failed', e);
    }
}

function updateUserUI(username) {
    const statusEl = document.getElementById('user-status');
    if (statusEl) statusEl.textContent = username;
    const btnLogin = document.getElementById('btn-login');
    if (btnLogin) btnLogin.classList.add('hidden');
    const btnLogout = document.getElementById('btn-logout');
    if (btnLogout) btnLogout.classList.remove('hidden');
}

function logout() {
    authToken = null;
    localStorage.removeItem('fraudshield_token');
    const statusEl = document.getElementById('user-status');
    if (statusEl) statusEl.textContent = 'Guest';
    const btnLogin = document.getElementById('btn-login');
    if (btnLogin) btnLogin.classList.remove('hidden');
    const btnLogout = document.getElementById('btn-logout');
    if (btnLogout) btnLogout.classList.add('hidden');
}

// ========== WEBSOCKET ALERTS ==========
function connectAlertWebSocket() {
    try {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const ws = new WebSocket(`${protocol}//${window.location.host}/ws/alerts`);

        ws.onmessage = (event) => {
            const alert = JSON.parse(event.data);
            showToast(alert);
            loadHistory();
        };

        ws.onclose = () => {
            setTimeout(connectAlertWebSocket, 3000);
        };

        ws.onerror = () => {
            ws.close();
        };
    } catch (e) {
        console.error('WebSocket connection failed', e);
    }
}

function showToast(alert) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
        <div class="toast-title">⚠️ Real-Time Fraud Alert — TX #${alert.transaction_id}</div>
        <div class="toast-body">
            Amount: $${parseFloat(alert.amount).toFixed(2)} |
            Disc: ${parseFloat(alert.discriminant_score).toFixed(4)} |
            SVM: ${parseFloat(alert.svm_score).toFixed(4)}
        </div>
    `;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
}

// ========== FEATURE IMPORTANCE ==========
let importanceData = null;

async function loadFeatureImportance() {
    try {
        const resp = await fetch('/api/feature-importance');
        if (!resp.ok) throw new Error('Failed to load');
        importanceData = await resp.json();
        renderImportanceModel('aggregate');
    } catch (e) {
        console.error('Feature importance error:', e);
    }
}

function renderImportanceModel(model) {
    if (!importanceData) return;
    const container = document.getElementById('importance-chart');
    if (!container) return;
    container.innerHTML = '';

    let items;
    if (model === 'aggregate') {
        items = importanceData.ranked.map(([name, val]) => ({name, importance: val}));
    } else {
        const modelData = importanceData[model];
        items = Object.entries(modelData)
            .map(([name, d]) => ({name, importance: d.importance, raw_weight: d.raw_weight}))
            .sort((a, b) => b.importance - a.importance);
    }

    const maxVal = Math.max(...items.map(i => i.importance));

    items.forEach(item => {
        const pct = (item.importance / maxVal) * 100;
        container.innerHTML += `
            <div class="imp-bar-row">
                <div class="imp-bar-label">${formatFeatureName(item.name)}</div>
                <div class="imp-bar-track">
                    <div class="imp-bar-fill" style="width: 0%" data-target-width="${pct}%"></div>
                </div>
                <div class="imp-bar-value">${(item.importance * 100).toFixed(1)}%</div>
            </div>
        `;
    });

    // Animate bars
    setTimeout(() => {
        container.querySelectorAll('.imp-bar-fill').forEach(bar => {
            bar.style.width = bar.getAttribute('data-target-width');
        });
    }, 50);
}

// ========== RETRAIN ==========
function downloadSampleTrainingCSV() {
    const csv = `amount,hour,merchant_risk,distance_from_home,transaction_velocity,is_international,is_fraud
45.00,14,0.15,5.0,1,0,0
2500.00,2,0.85,150.0,7,1,1
120.00,10,0.25,12.0,2,0,0
800.00,3,0.70,80.0,5,1,1
35.00,16,0.10,3.0,1,0,0
3200.00,1,0.90,200.0,8,1,1
67.50,11,0.20,8.5,1,0,0
950.00,23,0.65,95.0,6,1,1
28.00,15,0.12,4.0,1,0,0
1800.00,4,0.78,120.0,4,1,1
55.00,12,0.18,6.0,1,0,0
4500.00,3,0.92,250.0,9,1,1
90.00,9,0.22,10.0,2,0,0
1200.00,1,0.75,100.0,6,1,1
42.00,17,0.08,2.0,1,0,0
2800.00,22,0.88,180.0,8,1,1
75.00,13,0.16,7.0,1,0,0
600.00,4,0.60,60.0,4,1,1
30.00,10,0.14,4.5,1,0,0
1500.00,2,0.82,130.0,5,1,1`;
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'training_data.csv'; a.click();
    URL.revokeObjectURL(url);
}

async function retrainModels() {
    const file = document.getElementById('retrain-file').files[0];
    if (!file) return;

    const btn = document.getElementById('btn-retrain');
    btn.textContent = 'Retraining...';
    btn.disabled = true;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const resp = await fetch('/api/retrain', { method: 'POST', body: formData });
        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(err.detail || 'Retrain failed');
        }
        const data = await resp.json();
        renderRetrainResults(data);
    } catch (e) {
        alert('Retrain error: ' + e.message);
    } finally {
        btn.textContent = 'Retrain All Models';
        btn.disabled = false;
    }
}

function renderRetrainResults(data) {
    const summary = document.getElementById('retrain-summary');
    summary.innerHTML = `
        <div class="retrain-stat">
            <div class="stat-value text-safe">✓</div>
            <div class="stat-label">Status: ${data.status}</div>
        </div>
        <div class="retrain-stat">
            <div class="stat-value">${data.training_samples}</div>
            <div class="stat-label">Training Samples</div>
        </div>
        <div class="retrain-stat">
            <div class="stat-value">${data.test_samples}</div>
            <div class="stat-label">Test Samples</div>
        </div>
        <div class="retrain-stat">
            <div class="stat-value">${(data.fraud_ratio * 100).toFixed(1)}%</div>
            <div class="stat-label">Fraud Ratio</div>
        </div>
    `;

    const comparison = document.getElementById('retrain-comparison');
    comparison.innerHTML = '';

    const modelNames = {
        'discriminant': 'Discriminant', 'linear_svm': 'Linear SVM',
        'rbf_svm': 'RBF SVM', 'logistic': 'Logistic'
    };

    for (const [key, name] of Object.entries(modelNames)) {
        const before = data.before[key];
        const after = data.after[key];
        if (!before || !after) continue;

        const metrics = ['accuracy', 'precision', 'recall', 'f1'];
        let rows = metrics.map(m => {
            const bVal = (before[m] * 100).toFixed(1);
            const aVal = (after[m] * 100).toFixed(1);
            const diff = after[m] - before[m];
            const cls = diff > 0.001 ? 'val-improved' : diff < -0.001 ? 'val-declined' : '';
            const arrow = diff > 0.001 ? '↑' : diff < -0.001 ? '↓' : '=';
            return `<div class="comparison-row">
                <span>${m.charAt(0).toUpperCase() + m.slice(1)}</span>
                <span class="val-before">${bVal}%</span>
                <span class="val-after ${cls}">${aVal}% ${arrow}</span>
            </div>`;
        }).join('');

        comparison.innerHTML += `<div class="comparison-card"><h4>${name}</h4>${rows}</div>`;
    }

    document.getElementById('retrain-results').classList.remove('hidden');
}

// ========== ROI ==========
async function loadROI() {
    try {
        const resp = await fetch('/api/roi');
        if (!resp.ok) throw new Error('Failed to load ROI');
        const data = await resp.json();
        renderROI(data);
    } catch (e) {
        console.error('ROI error:', e);
    }
}

function renderROI(data) {
    const container = document.getElementById('roi-content');
    if (!container) return;
    const s = data.summary;
    const r = data.roi;
    const bm = data.best_model;

    container.innerHTML = `
        <div class="roi-grid">
            <div class="roi-card">
                <div class="roi-value">${s.total_transactions}</div>
                <div class="roi-label">Total Transactions</div>
            </div>
            <div class="roi-card">
                <div class="roi-value text-danger">${s.fraud_detected}</div>
                <div class="roi-label">Fraud Detected</div>
            </div>
            <div class="roi-card">
                <div class="roi-value text-safe">${s.legitimate}</div>
                <div class="roi-label">Legitimate</div>
            </div>
            <div class="roi-card">
                <div class="roi-value">${s.fraud_rate.toFixed(1)}%</div>
                <div class="roi-label">Fraud Rate</div>
            </div>
            <div class="roi-card">
                <div class="roi-value">$${s.total_amount.toFixed(0)}</div>
                <div class="roi-label">Total Amount</div>
            </div>
            <div class="roi-card">
                <div class="roi-value text-danger">$${s.fraud_amount.toFixed(0)}</div>
                <div class="roi-label">Fraud Amount</div>
            </div>
            <div class="roi-card highlight">
                <div class="roi-value text-safe">$${r.estimated_loss_prevented.toFixed(0)}</div>
                <div class="roi-label">Est. Loss Prevented</div>
            </div>
            <div class="roi-card highlight">
                <div class="roi-value text-safe">$${r.total_cost_prevented.toFixed(0)}</div>
                <div class="roi-label">Total Cost Prevented (3x)</div>
            </div>
        </div>
        <div style="margin-bottom: 1.5rem;">
            <h3 style="margin-bottom: 0.75rem;">Best Performing Model</h3>
            <div class="roi-grid" style="grid-template-columns: repeat(4, 1fr);">
                <div class="roi-card"><div class="roi-value" style="font-size:1rem;">${bm.name}</div><div class="roi-label">Model</div></div>
                <div class="roi-card"><div class="roi-value">${(bm.f1*100).toFixed(1)}%</div><div class="roi-label">F1 Score</div></div>
                <div class="roi-card"><div class="roi-value">${(bm.precision*100).toFixed(1)}%</div><div class="roi-label">Precision</div></div>
                <div class="roi-card"><div class="roi-value">${(bm.recall*100).toFixed(1)}%</div><div class="roi-label">Recall</div></div>
            </div>
        </div>
        <div class="roi-assumptions">
            <strong>📋 Assumptions:</strong><br>
            ${data.assumptions.map(a => '• ' + a).join('<br>')}
        </div>
    `;
}
