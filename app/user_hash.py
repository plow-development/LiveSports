from datetime import timedelta, datetime
from typing import Union

import asyncpg
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.queries.users import get_user
from app.config import SALT, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/login')

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SALT, algorithm=ALGORITHM)
    return encoded_jwt

def get_username_from_token(token: str, credentials_exception) -> str:
    try:
        payload = jwt.decode(token, SALT, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e
    return username

async def get_current_user(token: str = Depends(oauth2_scheme)) -> asyncpg.Record:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = get_username_from_token(token, credentials_exception)
    user = await get_user(username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_user_or_none(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = get_username_from_token(token, credentials_exception)
    user = await get_user(username)
    return user
