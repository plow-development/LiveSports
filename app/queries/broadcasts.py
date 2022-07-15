import asyncpg

from app.services.database import DataBase


async def add_broadcasts(title: str, description: str, preview: str, link: str):
    sql = """INSERT INTO broadcasts (title, description, preview, link) VALUES ($1, $2, $3, $4)"""
    await DataBase.execute(sql, title, description, preview, link)


async def broadcasts_list() -> list[asyncpg.Record]:
    sql = """SELECT id as broadcast_id, title, description, preview, link FROM broadcasts"""
    result = await DataBase.fetch(sql)
    return result
