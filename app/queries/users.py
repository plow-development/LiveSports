from datetime import date

import asyncpg

from app.exceptions import BadRequest, NotFound
from app.queries.teams import team_get
from app.services.database import DataBase


async def add_user(username: str, hashed_password: str, email: str, avatar: str,
                   firstname: str, lastname: str, birthday: date, money: int) -> None:
    """Создаёт пользователя в БД
    :param username: Псевдоним пользователя
    :param hashed_password: Хэшированный пароль
    :param email: Электронная почта пользователя
    :param avatar: Ссылка на аватар пользователя
    :param firstname: Имя пользователя
    :param lastname: Фамилия пользователя
    :param birthday: День Рожденья пользователя
    :param money: Баланс пользователя (в баллах)
    """
    sql = """
    INSERT INTO users (username, hashed_password, email, avatar, firstname, lastname, birthday, money)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    """
    try:
        await DataBase.execute(
            sql, username, hashed_password, email, avatar, firstname, lastname, birthday, money)
    except asyncpg.UniqueViolationError as e:
        raise BadRequest('Пользователь уже существует!') from e


async def get_user(username: str) -> asyncpg.Record:
    """Возвращает данные о пользователе
    :param username: Псевдоним пользователя
    """
    sql = """
    SELECT id as user_id, username, hashed_password, email, avatar, firstname, lastname, birthday, money
    FROM users
    WHERE username = ($1)
    """
    result = await DataBase.fetchrow(sql, username)
    if not result:
        raise NotFound('Пользователь не найден!')
    return result


async def get_username(user_id: int):
    """Возвращает ID пользователя из БД
    :param user_id: ID пользователя
    :return: username пользователя
    """
    sql = """SELECT username FROM users WHERE id = ($1)"""
    result = await DataBase.fetchval(sql, user_id)
    if not result:
        raise NotFound('Пользователь не найден!')
    return result


async def edit_user(
        user_id: int, username: str = None, email: str = None, avatar: str = None, firstname: str = None,
        lastname: str = None, birthday: date = None, money: int = None) -> None:
    user = await get_user(await get_username(user_id))
    if not username:
        username = user['username']
    if not email:
        email = user['email']
    if not avatar:
        avatar = user['avatar']
    if not firstname:
        firstname = user['firstname']
    if not lastname:
        lastname = user['lastname']
    if not birthday:
        birthday = user['birthday']
    if not money:
        money = user['money']
    sql = """
    UPDATE users
    SET username = ($1),
        email = ($2),
        avatar = ($3),
        firstname = ($4),
        lastname = ($5),
        birthday = ($6),
        money = ($7)
    WHERE id = ($8)
    """
    try:
        await DataBase.execute(
            sql, username, email, avatar, firstname, lastname, birthday, money, user_id)
    except asyncpg.UniqueViolationError as e:
        raise BadRequest('Этот псевдоним уже занят!') from e


async def get_user_team(user_id: int) -> list[asyncpg.Record]:
    """Возвращает из БД список команд, в которых состоит пользователь
    :param user_id: ID пользователя
    """
    sql = """SELECT team_id FROM teams_users WHERE user_id = $1"""
    team_ids = await DataBase.fetch(sql, user_id)
    teams = list()
    for team_id in team_ids:
        teams.append(await team_get(team_id))
    return teams


async def get_user_sports(user_id: int) -> list[asyncpg.Record]:
    """Возвращает список предпочитаемых видов спорта пользователя из БД
    :param user_id: ID пользователя
    """
    sql = """SELECT sports.name FROM user_sports
             left   join sports
             on     user_sports.sport_id = sports.id
             WHERE  user_sports.user_id = $1"""
    result = await DataBase.fetch(sql, user_id)
    return result


async def get_list_users() -> list[asyncpg.Record]:
    """Возвращает список пользователей из базы данных"""
    sql = """
    SELECT id as user_id, username, email, avatar, firstname, lastname, birthday, money
    FROM users
    """
    result = await DataBase.fetch(sql)
    return result


async def user_sport_add(user_id: int, sport_id: int) -> None:
    """Добавляет пользователю любимый вид спорта в БД
    :param user_id: ID пользователя
    :param sport_id: ID вида спорта
    """
    sql = """INSERT INTO user_sports (user_id, sport_id)
             VALUES ($1, $2)
             """
    try:
        await DataBase.execute(sql, user_id, sport_id)
    except asyncpg.UniqueViolationError as e:
        raise BadRequest(f'Вы уже выбирали этот вид спорта!') from e


async def user_sport_leave(user_id: int, sport_id: int) -> None:
    sql = """
    DELETE FROM user_sports
    WHERE user_id = ($1) and sport_id = ($2)
    """
    await DataBase.execute(sql, user_id, sport_id)



async def user_event_join(user_id: int, event_id: int, user_type: str) -> None:
    """
    Добавляет в БД тип участника на ивенте
    :param user_id: ID пользователя
    :param event_id: ID мероприятия
    :param user_type: Тип участника
    """
    sql = """
    INSERT INTO users_to_events (user_id, event_id, user_type)
    VALUES ($1, $2, $3)
    """
    try:
        await DataBase.execute(sql, user_id, event_id, user_type)
    except asyncpg.UniqueViolationError as e:
        raise BadRequest('Вы уже записаны на это мероприятие!') from e


async def user_event_leave(user_id: int, event_id: int) -> None:
    """
    Удаляет из БД посещение участника ивента
    :param user_id: ID пользователя
    :param event_id: ID мероприятия
    """
    # TODO: Check
    sql = """
    DELETE FROM users_to_events
    WHERE user_id = ($1) and event_id = ($2)
    """
    await DataBase.execute(sql, user_id, event_id)


async def del_user(user_id: int) -> None:
    """Удаляет пользователя из БД
    :param user_id: ID пользователя
    """
    sql = """DELETE FROM users WHERE id = ($1)"""
    await DataBase.execute(sql, user_id)
