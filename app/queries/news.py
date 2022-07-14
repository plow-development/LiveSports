import hashlib
from datetime import datetime

import asyncpg

from fastapi import UploadFile
from app.exceptions import NotFound
from app.queries.sports import get_sport
from app.services.database import DataBase


async def add_news(title: str, content: str, preview: UploadFile, publictime: datetime, user_id: int, sport_id: int):
    sql = """
    INSERT INTO news (title, content, preview, publictime, author_id, sport_id)
    VALUES ($1, $2, $3, $4, $5, $6)
    """
    if preview:
        image_data = preview.file.read()
        image_extension = preview.filename.split('.')[-1]
        image_name = f'resources/news_preview/{hashlib.sha224(image_data).hexdigest()}.{image_extension}'
        with open(image_name, mode='wb+') as image_file:
            image_file.write(image_data)
    else:
        image_name = None
    await get_sport(sport_id)  # Проверка существования вида спорта
    await DataBase.execute(sql, title, content, image_name, publictime, user_id, sport_id)


async def get_news(news_id: int) -> asyncpg.Record:
    sql = """
    SELECT id as news_id, title, content, preview, publictime, author_id, sport_id
    FROM news
    WHERE id = ($1)
    """
    result = await DataBase.fetchrow(sql, news_id)
    if not result:
        raise NotFound('Новость не найдена!')
    return result


async def news_list() -> list[asyncpg.Record]:
    sql = """
    SELECT id as news_id, title, content, preview, publictime, author_id, sport_id
    FROM news
    """
    result = await DataBase.fetch(sql)
    return result


async def news_list_by_interests(user_id: int) -> list[asyncpg.Record]:
    sql = """
    SELECT id as news_id, title, content, preview, publictime, author_id, sport_id
    FROM news
    WHERE sport_id IN (
        SELECT sport_id
        FROM user_sports
        WHERE user_id = ($1)
        )
    """
    result = await DataBase.fetch(sql, user_id)
    return result


async def del_news(news_id: int):
    await get_news(news_id)  # Optional
    sql = """
    DELETE FROM news
    WHERE id = ($1)
    """
    await DataBase.execute(sql, news_id)
