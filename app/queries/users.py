from datetime import date

import asyncpg

from app.exceptions import BadRequest, NotFound
from app.queries.teams import get_team
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
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)"""
    try:
        await DataBase.execute(
            sql, username, hashed_password, email, avatar, firstname, lastname, birthday, money)
    except asyncpg.UniqueViolationError as e:
        raise BadRequest("Пользователь уже существует!") from e


async def get_user(username: str) -> asyncpg.Record:
    """Возвращает данные о пользователе
    :param username: Псевдоним пользователя
    """
    sql = """SELECT id as user_id,
                    username,
                    hashed_password,
                    email,
                    avatar,
                    firstname,
                    lastname,
                    birthday,
                    money
             FROM users
             WHERE username = ($1)"""
    result = await DataBase.fetchrow(sql, username)
    if not result:
        raise NotFound("Пользователь не найден!")
    return result


async def get_username(user_id: int):
    sql = """SELECT username FROM users WHERE id = ($1)"""
    result = await DataBase.fetchval(sql, user_id)
    if not result:
        raise NotFound("Пользователь не найден!")
    return result


async def get_user_team(user_id: int) -> list[asyncpg.Record]:
    """Возвращает из БД список команд, в которых состоит пользователь
    :param user_id: ID пользователя
    """
    sql = """SELECT team_id FROM teams_users WHERE user_id = $1"""
    team_ids = await DataBase.fetch(sql, user_id)
    teams = list()
    for team_id in team_ids:
        teams.append(await get_team(team_id))
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
    sql = """SELECT id, username, email, avatar as avatar_url, firstname, lastname, birthday, money
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


async def del_user(user_id: int) -> None:
    """Удаляет пользователя из БД
    :param user_id: ID пользователя
    """
    sql = """DELETE FROM users
             WHERE id = ($1)
             """
    await DataBase.execute(sql, user_id)
