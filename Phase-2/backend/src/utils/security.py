from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status
import os
import hashlib

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password_bcrypt_safe(password: str) -> str:
    """Safely hash a password with bcrypt, handling the 72-byte limit."""
    # Encode to bytes
    password_bytes = password.encode('utf-8')

    # Bcrypt has a 72 byte limit, so truncate if necessary
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
        # Ensure we don't break UTF-8 encoding
        try:
            password = password_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # If truncation breaks UTF-8, decode with error handling
            password = password_bytes.decode('utf-8', errors='ignore')

    return pwd_context.hash(password)

def verify_password_bcrypt_safe(plain_password: str, hashed_password: str) -> bool:
    """Safely verify a password against its hash, handling the 72-byte limit."""
    # Encode to bytes
    password_bytes = plain_password.encode('utf-8')

    # Bcrypt has a 72 byte limit, so truncate if necessary
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
        # Ensure we don't break UTF-8 encoding
        try:
            plain_password = password_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # If truncation breaks UTF-8, decode with error handling
            plain_password = password_bytes.decode('utf-8', errors='ignore')

    return pwd_context.verify(plain_password, hashed_password)

# JWT configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-jwt-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its hash."""
    return verify_password_bcrypt_safe(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate a hash for the given password."""
    return hash_password_bcrypt_safe(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token with the given data."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify a JWT token and return its payload if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_user_id_from_token(token: str) -> Optional[str]:
    """Extract user ID from a JWT token."""
    payload = verify_token(token)
    if payload:
        return payload.get("sub")
    return None

def create_token_data(user_id: str, email: str) -> dict:
    """Create the data dictionary for a JWT token."""
    return {
        "sub": user_id,
        "email": email,
        "iat": datetime.utcnow(),
    }