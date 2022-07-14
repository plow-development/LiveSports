import asyncpg

from app.config import DATABASE_URL

class DataBase:
    pool: asyncpg.Pool

    @classmethod
    async def connect_db(cls):
        cls.pool = await asyncpg.create_pool(DATABASE_URL)

    @classmethod
    async def disconnect_db(cls):
        await cls.pool.close()

    @classmethod
    async def execute(cls, sql, *args) -> None:
        async with cls.pool.acquire() as con:
            await con.execute(sql, *args)

    @classmethod
    async def fetch(cls, sql, *args) -> list[asyncpg.Record]:
        async with cls.pool.acquire() as con:
            result = await con.fetch(sql, *args)
        return result

    @classmethod
    async def fetchrow(cls, sql, *args) -> asyncpg.Record:
        async with cls.pool.acquire() as con:
            result = await con.fetchrow(sql, *args)
        return result

    @classmethod
    async def fetchval(cls, sql, *args):
        async with cls.pool.acquire() as con:
            result = await con.fetchval(sql, *args)
        return result
