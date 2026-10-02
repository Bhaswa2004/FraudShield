from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import json
import asyncio
import numpy as np

router = APIRouter(prefix='/api')

# Will be set by main.py
model_manager = None
alert_manager = None

def set_model_manager(mm):
    global model_manager
    model_manager = mm

class TransactionInput(BaseModel):
    amount: float = Field(..., ge=0, description='Transaction amount in dollars')
    hour: float = Field(..., ge=0, le=23, description='Hour of transaction (0-23)')
    merchant_risk: float = Field(..., ge=0, le=1, description='Merchant risk score (0-1)')
    distance_from_home: float = Field(..., ge=0, description='Distance from home in km')
    transaction_velocity: float = Field(..., ge=1, description='Transactions in last hour')
    is_international: float = Field(..., ge=0, le=1, description='1 if international, 0 otherwise')

@router.post('/predict')
async def predict_transaction(txn: TransactionInput):
    '''Score a single transaction using all 4 models.
    Returns full math breakdown for each model.'''
    features = txn.model_dump()
    result = model_manager.predict(features)
    
    # Save to database
    from db.database import save_transaction
    txn_id = save_transaction(
        features,
        result['discriminant'],
        result['svm'],
        result['is_fraud_predicted']
    )
    result['transaction_id'] = txn_id
    
    # Broadcast WebSocket alert if fraud detected
    if result['is_fraud_predicted'] and alert_manager:
        from datetime import datetime
        alert_data = {
            'type': 'fraud_alert',
            'transaction_id': txn_id,
            'amount': features.get('amount'),
            'timestamp': datetime.now().isoformat(),
            'discriminant_score': result['discriminant']['raw_score'],
            'svm_score': result['svm']['decision_value'],
            'verdict': 'FRAUD'
        }
        asyncio.create_task(alert_manager.broadcast_alert(alert_data))
    
    return {
        'transaction_id': txn_id,
        'features': features,
        'discriminant': result['discriminant'],
        'svm': result['svm'],
        'rbf_svm': result.get('rbf_svm'),
        'logistic': result.get('logistic'),
        'is_fraud_predicted': result['is_fraud_predicted']
    }

@router.get('/history')
async def get_history():
    '''Return last 50 transactions from the database.'''
    from db.database import get_history
    rows = get_history(limit=50)
    # Parse JSON detail fields back to dicts
    for row in rows:
        if row.get('discriminant_details'):
            row['discriminant_details'] = json.loads(row['discriminant_details'])
        if row.get('svm_details'):
            row['svm_details'] = json.loads(row['svm_details'])
    return {'transactions': rows}

@router.get('/health')
async def health():
    return {'status': 'ok', 'models_loaded': model_manager is not None}

from fastapi import UploadFile, File

@router.post('/batch')
async def batch_predict(file: UploadFile = File(...)):
    '''Score a batch of transactions from CSV upload.'''
    from data_layer.csv_parser import parse_csv
    from db.database import save_transaction
    
    content = await file.read()
    try:
        transactions = parse_csv(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'CSV parse error: {str(e)}')
    
    results = []
    fraud_count = 0
    for i, txn in enumerate(transactions):
        result = model_manager.predict(txn)
        save_transaction(txn, result['discriminant'], result['svm'], result['is_fraud_predicted'])
        if result['is_fraud_predicted']:
            fraud_count += 1
            # Broadcast WebSocket alert for each fraud
            if alert_manager:
                from datetime import datetime
                alert_data = {
                    'type': 'fraud_alert',
                    'transaction_id': i + 1,
                    'amount': txn.get('amount'),
                    'timestamp': datetime.now().isoformat(),
                    'discriminant_score': result['discriminant']['raw_score'],
                    'svm_score': result['svm']['decision_value'],
                    'verdict': 'FRAUD'
                }
                asyncio.create_task(alert_manager.broadcast_alert(alert_data))
        results.append({
            'row': i + 1,
            'features': txn,
            'discriminant': result['discriminant'],
            'svm': result['svm'],
            'rbf_svm': result['rbf_svm'],
            'logistic': result['logistic'],
            'is_fraud_predicted': result['is_fraud_predicted']
        })
    
    return {
        'total': len(transactions),
        'fraud_count': fraud_count,
        'legit_count': len(transactions) - fraud_count,
        'results': results
    }

@router.get('/boundary')
async def get_boundary(kernel: str = 'linear'):
    '''Get 2D decision boundary data for kernel visualization.'''
    if kernel not in ('linear', 'rbf'):
        raise HTTPException(status_code=400, detail='kernel must be linear or rbf')
    return model_manager.get_boundary_data(kernel)

@router.get('/metrics')
async def get_metrics():
    '''Get precision, recall, F1, and confusion matrix for all models.'''
    return model_manager.get_metrics()

@router.get('/feature-importance')
async def get_feature_importance():
    '''Get feature importance scores from all models.'''
    return model_manager.get_feature_importance()

@router.post('/retrain')
async def retrain_models(file: UploadFile = File(...)):
    '''Retrain all models with new labeled dataset.
    CSV must have columns: amount, hour, merchant_risk, distance_from_home,
    transaction_velocity, is_international, is_fraud
    '''
    from data_layer.csv_parser import FEATURE_NAMES
    import csv
    import io
    
    content = await file.read()
    try:
        text = content.decode('utf-8-sig')
        reader = csv.DictReader(io.StringIO(text))
        rows = list(reader)
        
        if len(rows) < 20:
            raise HTTPException(status_code=400, detail='Need at least 20 rows for retraining')
        
        required = FEATURE_NAMES + ['is_fraud']
        for col in required:
            if col not in rows[0]:
                raise HTTPException(status_code=400, detail=f'Missing column: {col}')
        
        X = np.array([[float(row[f]) for f in FEATURE_NAMES] for row in rows])
        y = np.array([float(row['is_fraud']) for row in rows])
        
        unique_labels = np.unique(y)
        if len(unique_labels) < 2:
            raise HTTPException(status_code=400, detail='Dataset must contain both fraud and non-fraud examples')
        
        result = model_manager.retrain_with_data(X, y)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Retrain error: {str(e)}')

@router.get('/roi')
async def get_roi():
    '''Get ROI analysis based on transaction history.'''
    return model_manager.get_roi_analysis()

