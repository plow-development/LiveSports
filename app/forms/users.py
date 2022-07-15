from datetime import timedelta, date

import asyncpg
from fastapi import APIRouter, Depends, Form, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.config import TIMEOUT
from app.exceptions import BadRequest
from app.models.models import UserComplex, UserOut, TeamOut, SportOut
from app.queries.users import add_user, get_user_team, get_user, get_user_sports, get_list_users, del_user
from app.user_hash import get_password_hash, verify_password, create_access_token, get_current_user
from app.utils.utils import format_record, format_records

router_users = APIRouter(tags=['Пользователи'])


@router_users.post("/user/registration")
async def User_registration(
        request: OAuth2PasswordRequestForm = Depends(),
        email: EmailStr = Form(..., description='Почта пользователя'),
        avatar: str = Form(..., description='Аватарка пользователя'),
        firstname: str = Form(..., description='Имя пользователя'),
        lastname: str = Form(..., description='Фамилия пользователя'),
        birthday: date = Form(..., description='День Рожденья пользователя'),
        money: int = Form(..., description='Баллы пользователя')) -> JSONResponse:
    """
    Регистрация пользователя

    :param request: Псевдоним и пароль пользователя<br>
    :param email: Почта пользователя<br>
    :param avatar: Аватарка пользователя<br>
    :param firstname: Имя пользователя<br>
    :param lastname: Фамилия пользователя<br>
    :param birthday: День Рожденья пользователя<br>
    :param money: Баллы пользователя<br>
    :return: JSONResponse HTTP_201_CREATED {'access_token': access_token, 'token_type': 'bearer'}
    """
    username = request.username
    hashed_password = get_password_hash(request.password)
    await add_user(username=username, hashed_password=hashed_password, email=email, avatar=avatar, firstname=firstname,
                   lastname=lastname, birthday=birthday, money=money)
    timeout = timedelta(minutes=TIMEOUT)
    access_token = create_access_token(data={'sub': username}, expires_delta=timeout)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'access_token': access_token, 'token_type': 'bearer'})


@router_users.post('/user/login')
async def User_authorization(request: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    """
    Авторизация пользователя

    :param request: Псевдоним и пароль пользователя<br>
    :return: JSONResponse HTTP_200_OK {'access_token': access_token, 'token_type': 'bearer'}
    """
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


@router_users.get('/user', response_model=UserComplex)
async def User_information(user: asyncpg.Record = Depends(get_current_user)):
    """
    Получение информации о пользователе  <br>
    :param user: Авторизованный пользователь  <br>
    :return: Модель UserComplex  <br>
    """
    return UserComplex(
        user=format_record(user, UserOut),
        team=format_records(await get_user_team(user['user_id']), TeamOut),
        sport_type_out=format_records(await get_user_sports(user['user_id']), SportOut)
    )


@router_users.get('/users/list', response_model=list[UserComplex])
async def List_of_users():
    """
    Получение списка информации о пользователе

    :return: Модель UserComplexInList
    """
    users = await get_list_users()
    list_of_user_complex_in_list = list()
    for user in users:
        list_of_user_complex_in_list.append(UserComplex(
            user=format_record(user, UserOut),
            team=format_records(await get_user_team(user['id']), TeamOut),
            sport_type=format_records(await get_user_sports(user['id']), SportOut)
        ))
    return list_of_user_complex_in_list

@router_users.delete('/user/del')
async def Deleting_User(
        user: asyncpg.Record = Depends(get_current_user)) -> JSONResponse:
    """
    Самоудаление пользователя

    :param user: Авторизованный пользователь<br>
    :return: JSONResponse HTTP_202_ACCEPTED
    """
    user_id: int = (await get_user(user['username']))['user_id']
    await del_user(user_id)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={'message': 'Вы успешно удалили свой аккаунт!'}
    )
