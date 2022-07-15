from datetime import timedelta, date

import asyncpg
from fastapi import APIRouter, Depends, Form, status, Query
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.config import TIMEOUT
from app.exceptions import BadRequest
from app.models.models import UserComplex, UserOut, TeamOut, SportOut, Created, Updated, Joined, Deleted
from app.queries.sports import get_sport
from app.queries.teams import team_get
from app.queries.users import add_user, get_user, get_username, edit_user, get_user_team, get_user_sports, \
    get_list_users, user_sport_add, del_user, user_sport_leave, user_team_join, user_team_list, user_team_leave
from app.user_hash import get_password_hash, verify_password, create_access_token, get_current_user
from app.utils.utils import format_record, format_records

router_users = APIRouter(tags=['Пользователи'])


@router_users.post("/user/register")
async def User_Register(
        request: OAuth2PasswordRequestForm = Depends(),
        email: EmailStr = Form(..., description='Почта пользователя'),
        avatar: str = Form(..., description='Аватарка пользователя'),
        firstname: str = Form(..., description='Имя пользователя'),
        lastname: str = Form(..., description='Фамилия пользователя'),
        birthday: date = Form(..., description='День Рожденья пользователя'),
        money: int = Form(..., description='Баллы пользователя')) -> JSONResponse:
    """
    Регистрация пользователя  <br>
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
async def User_Login(request: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    """
    Авторизация пользователя  <br>
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


@router_users.get('/user/get', response_model=UserComplex)
async def User_Info(user: asyncpg.Record = Depends(get_current_user)):
    """
    Получение информации о пользователе.  <br>
    Пользователь должен быть авторизован!  <br>
    """
    return UserComplex(
        user=format_record(user, UserOut),
        team=format_records(await get_user_team(user['user_id']), TeamOut),
        sport_type_out=format_records(await get_user_sports(user['user_id']), SportOut)
    )


@router_users.post('/user/edit', response_model=Updated)
async def User_Editing(
        user: asyncpg.Record = Depends(get_current_user),
        username: str = Form(None, description='Логин пользователя'),
        email: EmailStr = Form(None, description='Почта пользователя'),
        avatar: str = Form(None, description='Аватарка пользователя'),
        firstname: str = Form(None, description='Имя пользователя'),
        lastname: str = Form(None, description='Фамилия пользователя'),
        birthday: date = Form(None, description='День Рожденья пользователя'),
        money: int = Form(None, description='Баллы пользователя')):
    """
    Редактирование данных пользователя.  <br>
    Пользователь должен быть авторизован!  <br>
    """
    await edit_user(
        user_id=user['user_id'],
        username=username,
        email=email,
        avatar=avatar,
        firstname=firstname,
        lastname=lastname,
        birthday=birthday,
        money=money
    )
    return Updated()


@router_users.get('/user/list', response_model=list[UserComplex])
async def List_of_users():
    """
    Получение списка пользователей
    """
    list_users = await get_list_users()
    out_list = list()
    for user in list_users:
        list_teams = await get_user_team(user['user_id'])
        list_sports = await get_user_sports(user['user_id'])
        out_list.append(UserComplex(
            user=format_record(user, UserOut),
            team=format_records(list_teams, TeamOut),
            sport_type=format_records(list_sports, SportOut)
        ))
    return out_list


@router_users.post('/user/sport/add', response_model=Joined)
async def User_Sport_Add(
        user: asyncpg.Record = Depends(get_current_user),
        sport_id: int = Form(..., description='ID вида спорта')):
    """
    Добавление предпочтительного вида спорта.  <br>
    Пользователь должен быть авторизован!  <br>
    :param user:
    :param sport_id:
    :return:
    """
    await get_sport(sport_id)  # Check
    await user_sport_add(
        user_id=user['user_id'],
        sport_id=sport_id
    )
    return Joined()


@router_users.post('/user/sport/leave')
async def User_spoer_leave(
        user: asyncpg.Record = Depends(get_current_user),
        sport_id: int = Form(..., description='ID вида спорта')):
    await user_sport_leave(user_id=user['user_id'], sport_id=sport_id)


@router_users.delete('/user/del', response_model=Deleted)
async def Deleting_User(user: asyncpg.Record = Depends(get_current_user)):
    """
    Самоудаление пользователя.  <br>
    Пользователь должен быть авторизован!  <br>
    """
    await del_user(
        user_id=user['user_id']
    )
    return Deleted()


@router_users.post('/user/team/join', response_model=Joined)
async def User_Team_Join(
        user: asyncpg.Record = Depends(get_current_user),
        team_id: int = Query(..., description='ID команды')):
    await user_team_join(user_id=user['user_id'], team_id=team_id)
    return Joined()


# @router_users.get('/user/team/list', response_model=TeamOut)
# async def User_Team_List(
#         user: asyncpg.Record = Depends(get_current_user)):
#     list_team = await user_team_list(user_id=user['user_id'])
#     out = list()
#     for ttt in list_team:
#         out.append(await team_get(ttt['team_id']))
#     return format_records(out, TeamOut)


@router_users.post('/user/team/leave')
async def User_Team_Leave(
        user: asyncpg.Record = Depends(get_current_user),
        team_id: int = Query(..., description='ID команды')):
    await user_team_leave(user_id=user['user_id'], team_id=team_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Вы успешно вышли из команды'})
