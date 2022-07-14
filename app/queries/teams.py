import asyncpg

from app.exceptions import BadRequest, NotFound, Forbidden
from app.services.database import DataBase


async def add_team(team_name: str, user_id: int, sport_id: int) -> None:
    """Добавление команды в БД
    :param team_name: Название команды
    :param user_id: ID пользователя - владельца команды
    :param sport_id: ID вида спорта команды
    """
    sql = """INSERT INTO teams (name, master_id, sport_id) VALUES ($1, $2, $3)"""
    await DataBase.execute(sql, team_name, user_id, sport_id)


async def get_team(team_id: int) -> asyncpg.Record:
    """Получение информации о команде из БД
    :param team_id: ID группы
    :return: name, master_id, sport_id команды
    """
    sql = """SELECT name, master_id, sport_id FROM teams WHERE id = $1"""
    result = await DataBase.fetchrow(sql, team_id)
    if not result:
        raise NotFound('Команда не существует!')
    return result


async def get_list_team() -> list[asyncpg.Record]:
    """Получение списка команд.
    Для разработчиков
    :return: Список команд (id, name, master_id, sport_id)
    """
    sql = """SELECT id, name, master_id, sport_id FROM teams"""
    result = await DataBase.fetch(sql)
    return result


async def _is_master_(team_id: int, user_id: int) -> None:
    """Проверяет, является ли пользователь владельцем команды.
    Для разработки
    :param team_id: ID группы
    :param user_id: ID пользователя
    """
    sql = """SELECT master_id FROM teams WHERE id = $1"""
    master_id = await DataBase.fetchval(sql, team_id)
    if master_id != user_id:
        raise Forbidden('Вы не являетесь владельцем этой команды!')


async def del_team(team_id: int, user_id: int):
    """Удаляет команду из БД
    :param team_id: ID группы
    :param user_id: ID пользователя
    """
    await _is_master_(team_id, user_id)
    sql = """DELETE FROM teams WHERE id = ($1)"""
    await DataBase.execute(sql, team_id)
