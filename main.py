from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_layer.routes import router, set_model_manager
from api_layer.auth_routes import auth_router
from api_layer.websocket_manager import alert_manager
from model_layer.model_manager import ModelManager
from db.database import init_db
from db.auth import init_auth_db
from fastapi import WebSocket, WebSocketDisconnect

app = FastAPI(
    title='FraudShield',
    description='Financial Fraud Intelligence — ML Classification Demo',
    version='2.0.0'
)

# Initialize databases
init_db()
init_auth_db()

# Initialize and train models
print('Initializing models...')
mm = ModelManager()
set_model_manager(mm)
print('Models ready.')

# Register API routes
app.include_router(router)
app.include_router(auth_router)

# Make alert_manager accessible to routes
import api_layer.routes as routes_module
routes_module.alert_manager = alert_manager

# WebSocket endpoint (must be before static mount)
@app.websocket('/ws/alerts')
async def websocket_endpoint(websocket: WebSocket):
    await alert_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        alert_manager.disconnect(websocket)

# Serve frontend (must be last)
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')

@app.get('/')
async def serve_index():
    return FileResponse(os.path.join(frontend_dir, 'index.html'))

app.mount('/static', StaticFiles(directory=frontend_dir), name='static')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
