import asyncpg

from app.exceptions import NotFound, Forbidden
from app.services.database import DataBase


async def team_add(
        team_name: str, user_id: int, sport_id: int
) -> None:
    """
    Добавление в БД команды
    :param team_name: Название команды
    :param user_id: ID пользователя - владельца команды
    :param sport_id: ID вида спорта команды
    """
    sql = """
    INSERT INTO teams (name, master_id, sport_id)
    VALUES ($1, $2, $3)
    """
    await DataBase.execute(sql, team_name, user_id, sport_id)


async def team_edit(
        team_id: int, user_id: int, team_name: str = None, master_id: int = None, sport_id: int = None
) -> None:
    """
    Редактирование БД команды
    :param team_id: ID команды, которую будут обновлять
    :param user_id: ID пользователя - владельца команды
    :param team_name: Название команды
    :param master_id: Новый ID нового владельца команды
    :param sport_id: Новый ID вида спорта команды
    """
    await _is_master_(team_id=team_id, user_id=user_id)  # Check
    old_team = await team_get(team_id=team_id)  # Check
    if not team_name:
        team_name = old_team['name']
    if not master_id:
        master_id = old_team['master_id']
    if not sport_id:
        sport_id = old_team['sport_id']
    sql = """
    UPDATE teams
    SET name = ($1),
        master_id = ($2),
        sport_id = ($3)
    WHERE id = ($4)
    """
    await DataBase.execute(sql, team_name, master_id, sport_id, team_id)


async def team_get(
        team_id: int
) -> asyncpg.Record:
    """
    Получение из БД информации о команде
    :param team_id: ID команды
    :return: team_id, name, master_id, sport_id команды
    """
    sql = """
    SELECT id as team_id, name, master_id, sport_id
    FROM teams
    WHERE id = ($1)
    """
    result = await DataBase.fetchrow(sql, team_id)
    if not result:
        raise NotFound('Команда не найдена!')
    return result


async def team_get_list() -> list[asyncpg.Record]:
    """
    Получение списка команд
    :return: Список команд (id, name, master_id, sport_id)
    """
    sql = """
    SELECT id as team_id, name, master_id, sport_id
    FROM teams
    """
    result = await DataBase.fetch(sql)
    return result


async def get_team_list_user(team_id: int):
    """
    Возвращает список ID пользователей из БД в определённой команде
    """
    sql = """SELECT user_id FROM teams_users WHERE team_id = $1"""
    result = await DataBase.fetch(sql, team_id)
    return result


async def _is_master_(team_id: int, user_id: int) -> None:
    """
    Проверяет, является ли пользователь владельцем команды
    :param team_id: ID команды
    :param user_id: ID пользователя
    """
    sql = """
    SELECT master_id
    FROM teams
    WHERE id = $1
    """
    master_id = await DataBase.fetchval(sql, team_id)
    if master_id != user_id:
        raise Forbidden('Вы не являетесь владельцем этой команды!')


async def del_team(team_id: int, user_id: int):
    """
    Удаляет из БД команду
    :param team_id: ID команды
    :param user_id: ID пользователя
    """
    await _is_master_(team_id=team_id, user_id=user_id)  # Check
    sql = """
    DELETE FROM teams
    WHERE id = ($1)
    """
    await DataBase.execute(sql, team_id)
