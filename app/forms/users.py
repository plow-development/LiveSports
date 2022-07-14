from datetime import datetime, timedelta

import asyncpg
from fastapi import APIRouter, Depends, Form, status, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.config import TIMEOUT
from app.exceptions import BadRequest
from app.queries.users import add_user, get_user_team, get_user, get_list_users, user_sport_add
from app.user_hash import get_password_hash, verify_password, create_access_token, get_current_user
from app.utils.utils import format_record, format_records

router_users = APIRouter(tags=['Пользователи'])

@router_users.post("/user/registration")
async def User_registration(
        request: OAuth2PasswordRequestForm = Depends(),
        email: EmailStr = Form(..., description='Почта пользователя'),
        image: UploadFile = File(..., description='Аватарка пользователя'),
        firstname: str = Form(..., description='Имя пользователя'),
        lastname: str = Form(..., description='Фамилия пользователя'),
        birthday: datetime = Form(..., description='День Рожденья пользователя'),
        type_: str = Form(..., description='Тип пользователя'),
        money: int = Form(..., description='Баллы пользователя')
):
    username = request.username
    hashed_password = get_password_hash(request.password)
    await add_user(username=username, hashed_password=hashed_password, email=email, image=image, firstname=firstname,
                   lastname=lastname, birthday=birthday, type_=type_, money=money)
    timeout = timedelta(minutes=TIMEOUT)
    access_token = create_access_token(data={'sub': username}, expires_delta=timeout)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'access_token': access_token, 'token_type': 'bearer'})

@router_users.post('/user/login')
async def User_authorization(request: OAuth2PasswordRequestForm = Depends()):
    username = request.username
    user = await get_user(username)
    password = request.password
    if not verify_password(password, user['hashed_password']):
        raise BadRequest('Неверный пароль')
    timeout = timedelta(minutes=TIMEOUT)
    access_token = create_access_token(data={'sub': username}, expires_delta=timeout)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'access_token': access_token, 'token_type': 'bearer'})
