import hashlib

import asyncpg
from fastapi import UploadFile

from app.services.database import DataBase


async def add_broadcasts(title: str, description: str, preview: UploadFile, link: str):
    sql = """
    INSERT INTO broadcasts (title, description, preview, link)
    VALUES ($1, $2, $3, $4)
    """
    if preview:
        image_data = preview.file.read()
        image_extension = preview.filename.split('.')[-1]
        image_name = f'resources/broadcasts_preview/{hashlib.sha224(image_data).hexdigest()}.{image_extension}'
        with open(image_name, mode='wb+') as image_file:
            image_file.write(image_data)
    else:
        image_name = None
    await DataBase.execute(sql, title, description, image_name, link)


async def broadcasts_list() -> list[asyncpg.Record]:
    sql = """
    SELECT id as broadcast_id, title, description, preview, link
    FROM broadcasts
    """
    result = await DataBase.fetch(sql)
    return result
