import hashlib
from datetime import datetime

import asyncpg

from fastapi import UploadFile
from app.exceptions import NotFound
from app.services.database import DataBase


async def add_news(title: str, content: str, preview: UploadFile, publictime: datetime, user_id: int) -> None:
    sql = """
    INSERT INTO news (title, content, preview, publictime, author_id)
    VALUES ($1, $2, $3, $4, $5)"""
    if preview:
        image_data = preview.file.read()
        image_extension = preview.filename.split('.')[-1]
        image_name = f'resources/avatars/{hashlib.sha224(image_data).hexdigest()}.{image_extension}'
        with open(image_name, mode='wb+') as image_file:
            image_file.write(image_data)
    else:
        image_name = None
    await DataBase.execute(sql, title, content, image_name, publictime, user_id)


async def get_news(news_id: int) -> asyncpg.Record:
    sql = """
    SELECT id as user_id, title, content, preview, publictime, author_id
    FROM news
    WHERE id = ($1)
    """
    result = await DataBase.fetchrow(sql, news_id)
    if not result:
        raise NotFound('Новость не найдена!')
    return result


async def del_news(news_id: int) -> None:
    await get_news(news_id)  # Optional
    sql = """DELETE FROM news WHERE id = ($1)"""
    await DataBase.execute(sql, news_id)
