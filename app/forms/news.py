from datetime import datetime

import asyncpg
from fastapi import APIRouter, Depends, Form, status, UploadFile, Query, File
from fastapi.responses import JSONResponse

from app.models.models import NewsOut
from app.queries.news import add_news, get_news, news_list, news_list_by_interests, del_news
from app.user_hash import get_current_user
from app.utils.utils import format_records

router_news = APIRouter(tags=['Новости'])


@router_news.post('/news/create')
async def Creating_news(
        title: str = Form(..., description='Заголовок новости'),
        content: str = Form(..., description='Текст новости'),
        preview: UploadFile = File(..., description='Картинка новости'),
        publictime: datetime = Form(..., description='Время написания новости'),
        user_agent: asyncpg.Record = Depends(get_current_user),
        sport_id: int = Form(..., description='ID вида спорта')) -> JSONResponse:
    await add_news(title, content, preview, publictime, user_agent['user_id'], sport_id)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': f'Новость «{title}» успешно опубликована!'})


@router_news.get('/news/list', response_model=list[NewsOut])
async def List_of_news():
    return format_records(await news_list(), NewsOut)


@router_news.get('/news/list_by_interests', response_model=list[NewsOut])
async def List_of_news_by_interests(user_id: int):
    return format_records(await news_list_by_interests(user_id), NewsOut)
