from datetime import datetime, date

import asyncpg
import hashlib

from fastapi import UploadFile
from app.exceptions import BadRequest, NotFound
from app.services.database import DataBase


async def add_user(username: str, hashed_password: str, email: str, image: UploadFile,
                   firstname: str, lastname: str, birthday: date, money: int) -> None:
    """Создаёт пользователя в БД
    :param username: Псевдоним пользователя
    :param hashed_password: Хэшированный пароль
    :param email: Электронная почта пользователя
    :param image: Ссылка на аватар пользователя
    :param firstname: Имя пользователя
    :param lastname: Фамилия пользователя
    :param birthday: День Рожденья пользователя
    :param money: Баланс пользователя (в баллах)
    """
    sql = """INSERT INTO users (username, hashed_password, email, avatar, firstname, lastname, birthday, money)
             VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
             """
    if image:
        image_data = image.file.read()
        image_extension = image.filename.split('.')[-1]
        image_name = f'resources/avatars/{hashlib.sha224(image_data).hexdigest()}.{image_extension}'
        with open(image_name, mode='wb+') as image_file:
            image_file.write(image_data)
    else:
        image_name = None
    try:
        await DataBase.execute(
            sql, username, hashed_password, email, image_name, firstname, lastname, birthday, money)
    except asyncpg.UniqueViolationError as e:
        raise BadRequest("Пользователь уже существует!") from e


async def get_user(username: str) -> asyncpg.Record:
    """Возвращает данные о пользователе:
    username, hashed_password, email, avatar_url, firstname, lastname, birthday, money
    :param username: Псевдоним пользователя
    """
    sql = """SELECT username, hashed_password, email, avatar as avatar_url, firstname, lastname, birthday, money
             FROM users
             WHERE username = $1
             """
    result = await DataBase.fetch(sql, username)
    if not result:
        raise NotFound("Пользователь не существует!")
    return result[0]


async def get_user_id(username: str) -> int:
    """Получение ID пользователя по его псевдониму
    :param username: Псевдоним пользователя
    """
    sql = """SELECT id
             FROM users
             WHERE username = $1
             """
    result = await DataBase.fetchval(sql, username)
    if not result:
        raise NotFound("Пользователь не существует!")
    return result


async def get_user_team(user_id: int) -> list[asyncpg.Record]:
    """Возвращает из БД список команд, в которых состоит пользователь
    :param user_id: ID пользователя
    """
    sql = """SELECT teams.name FROM teams_users
             left   join teams
             on     teams_users.team_id = teams.id
             WHERE  teams_users.user_id = $1
             """
    result = await DataBase.fetch(sql, user_id)
    return result


async def get_user_sports(user_id: int) -> list[asyncpg.Record]:
    """Возвращает список предпочитаемых видов спорта пользователя из БД
    :param user_id: ID пользователя
    """
    sql = """SELECT sports.name FROM user_sports
             left   join sports
             on     user_sports.sport_id = sports.id
             WHERE  user_sports.user_id = $1
             """
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
