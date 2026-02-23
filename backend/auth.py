from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
import models

# Security configuration
SECRET_KEY = "your-secret-key-change-in-production" # Change this in production
ALGORITHM = "HS"
ACCESS_TOKEN_EXPIRE_MINUTES = 0

# Password hashing
pwd_context = CryptContext(schemes=["pbkdf_sha"], deprecated="auto")

# Token security
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
 """Verify a password against its hash"""
 return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
 """Hash a password"""
 return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
 """Create JWT access token"""
 to_encode = data.copy()
 if expires_delta:
 expire = datetime.utcnow() + expires_delta
 else:
 expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

 to_encode.update({"exp": expire})
 encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
 return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
 """Verify JWT token"""
 token = credentials.credentials
 credentials_exception = HTTPException(
 status_code=status.HTTP_0_UNAUTHORIZED,
 detail="Could not validate credentials",
 headers={"WWW-Authenticate": "Bearer"},
 )

 try:
 payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
 email: str = payload.get("sub")
 if email is None:
 raise credentials_exception
 return email
 except JWTError:
 raise credentials_exception

def get_current_user(
 email: str = Depends(verify_token),
 db: Session = Depends(get_db)
):
 """Get current user from token"""
 user = db.query(models.User).filter(models.User.email == email).first()
 if user is None:
 raise HTTPException(
 status_code=status.HTTP_0_UNAUTHORIZED,
 detail="User not found"
 )
 return user

def authenticate_user(email: str, password: str, db: Session):
 """Authenticate user with email and password"""
 user = db.query(models.User).filter(models.User.email == email).first()
 if not user:
 return False
 if not verify_password(password, user.password_hash):
 return False
 return user