from datetime import date, datetime

import asyncpg

from app.services.database import DataBase


async def add_event(name: str, description: str, preview: str, starttime: datetime,
                    latitude: float, longitude: float, sport_id: int):
    sql = """
    INSERT INTO events (name, description, preview, starttime, latitude, longitude, sport_id)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    """
    await DataBase.execute(sql, name, description, preview, starttime, latitude, longitude, sport_id)


async def get_event(event_id: int):
    sql = """
    SELECT id as event_id, name, description, preview, starttime, latitude, longitude, sport_id
    FROM events
    WHERE id = ($1)
    """
    result = await DataBase.fetch(sql, event_id)
    return result


async def events_list() -> list[asyncpg.Record]:
    sql = """
    SELECT id as event_id, name, description, preview, starttime, latitude, longitude, sport_id
    FROM events
    """
    result = await DataBase.fetch(sql)
    return result


async def events_list_by_datetime(starttime: date) -> list[asyncpg.Record]:
    sql = """
    SELECT id as event_id, name, description, preview, starttime, latitude, longitude, sport_id
    FROM events
    WHERE date_trunc('days', starttime) = ($1)
    """
    result = await DataBase.fetch(sql, starttime)
    return result
