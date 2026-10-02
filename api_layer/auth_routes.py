from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from db.auth import register_user, authenticate_user, verify_token, get_current_user

auth_router = APIRouter(prefix='/api/auth')

class AuthRequest(BaseModel):
    username: str
    password: str

@auth_router.post('/register')
async def register(req: AuthRequest):
    try:
        result = register_user(req.username, req.password)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post('/login')
async def login(req: AuthRequest):
    try:
        token = authenticate_user(req.username, req.password)
        return {'token': token, 'username': req.username, 'message': 'Login successful'}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@auth_router.get('/me')
async def me(request: Request):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Not authenticated')
    token = auth_header.split(' ')[1]
    try:
        username = get_current_user(token)
        return {'username': username}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
