import asyncpg

from app.exceptions import BadRequest, NotFound
from app.services.database import DataBase


async def add_sport(name: str, description: str, sport_type: str) -> None:
    """
    Создаёт вид спорта в БД

    :param name: Название вида спорта
    :param description: Описание вида спорта
    :param sport_type: Тип вида спорта
    :return: None
    """
    sql = """INSERT INTO sports(name, description, type) VALUES ($1,$2,$3)"""
    try:
        await DataBase.execute(sql, name, description, sport_type)
    except asyncpg.UniqueViolationError as e:
        raise BadRequest(f'Вид спорта с названием «{name}» уже существует!') from e


async def get_sport(sport_id: int) -> asyncpg.Record:
    """
    Получение информации о виде спорта из БД по его ID

    :param sport_id: ID вида спорта
    :return: Множество ячеек подходящей строки таблицы sports
    """
    sql = """SELECT name, description, type as sport_type
             FROM sports
             WHERE id = $1
             """
    result = await DataBase.fetch(sql, sport_id)
    if not result:
        raise NotFound("Пользователь не существует!")
    return result[0]


async def get_sport_id(name: str) -> int:
    """
    Получает ID вида спорта из БД по его названию

    :param name: Название вида спорта
    :return: ID вида спорта
    """
    sql = """SELECT id FROM sports WHERE name = $1"""
    result = await DataBase.fetchval(sql, name)
    if not result:
        raise NotFound(f'Вида спорта с названием «{name}» не найдено!')
    return result

async def get_sport_name(sport_id: int) -> str:
    """
    Получает название вида спорта из БД по его ID

    :param sport_id: ID вида спорта
    :return: Название вида спорта
    """
    sql = """SELECT name FROM sports WHERE id = $1"""
    result = await DataBase.fetchval(sql, sport_id)
    if not result:
        raise NotFound(f'Вида спорта с ID {sport_id} не найден!')
    return result

async def get_list_sport() -> list[asyncpg.Record]:
    """
    :return: Список видов спорта из БД
    """
    sql = """SELECT name, description, type FROM sports"""
    result = await DataBase.fetch(sql)
    return result
