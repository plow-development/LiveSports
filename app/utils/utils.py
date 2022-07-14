from typing import Type

import asyncpg
from pydantic import BaseModel

def format_record(record: asyncpg.Record, model: Type[BaseModel]) -> BaseModel | None:
    if not record:
        return None
    return model(**record)

def format_records(records: list[asyncpg.Record], model: Type[BaseModel]) -> list[BaseModel]:
    if not records:
        return list()
    return list(map(lambda x: format_record(x, model), records))
