import sqlite3
import bcrypt
import jwt
import os
from datetime import datetime, timedelta, timezone

# Import DB_PATH from existing database module
from db.database import DB_PATH

SECRET_KEY = os.environ.get('FRAUDSHIELD_SECRET', 'fraudshield-dev-secret-key-2024')
ALGORITHM = 'HS256'
TOKEN_EXPIRY_HOURS = 24

def init_auth_db():
    """Create users table if not exists."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL,
        last_login TEXT
    )''')
    conn.commit()
    conn.close()

def register_user(username: str, password: str) -> dict:
    """Register a new user. Returns user dict or raises ValueError."""
    if len(username) < 3:
        raise ValueError('Username must be at least 3 characters')
    if len(password) < 6:
        raise ValueError('Password must be at least 6 characters')
    
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            'INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)',
            (username, password_hash, datetime.now(timezone.utc).isoformat())
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise ValueError('Username already exists')
    conn.close()
    
    return {'username': username, 'message': 'Registration successful'}

def authenticate_user(username: str, password: str) -> str:
    """Authenticate and return JWT token, or raise ValueError."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    
    if not row:
        conn.close()
        raise ValueError('Invalid username or password')
    
    if not bcrypt.checkpw(password.encode('utf-8'), row['password_hash'].encode('utf-8')):
        conn.close()
        raise ValueError('Invalid username or password')
    
    # Update last login
    conn.execute('UPDATE users SET last_login = ? WHERE id = ?',
                 (datetime.now(timezone.utc).isoformat(), row['id']))
    conn.commit()
    conn.close()
    
    # Generate JWT token
    payload = {
        'sub': username,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRY_HOURS)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str) -> dict:
    """Verify JWT token and return payload. Raises ValueError if invalid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token has expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')

def get_current_user(token: str) -> str:
    """Extract username from a valid token."""
    payload = verify_token(token)
    return payload['sub']
