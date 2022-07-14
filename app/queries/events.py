from datetime import datetime

import asyncpg

from app.services.database import DataBase


async def add_event(name: str, starttime: datetime, latitude: float, longitude: float):
    sql = """
    INSERT INTO events (name, starttime, latitude, longitude)
    VALUES ($1, $2, $3, $4)
    """
    await DataBase.execute(sql, name, starttime, latitude, longitude)


async def get_event(event_id: int):
    sql = """
    SELECT id as event_id, name, starttime, latitude, longitude
    FROM events
    WHERE id = ($1)
    """
    result = await DataBase.fetch(sql, event_id)
    return result


async def events_list() -> list[asyncpg.Record]:
    sql = """
    SELECT id as event_id, name, starttime, latitude, longitude
    FROM events
    """
    result = await DataBase.fetch(sql)
    return result


async def events_list_by_datetime(starttime: datetime) -> list[asyncpg.Record]:
    sql = """
    SELECT id as event_id, name, starttime, latitude, longitude
    FROM events
    WHERE starttime = ($1)
    """
    result = await DataBase.fetch(sql, starttime)
    return result
