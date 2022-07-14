from datetime import datetime

import asyncpg
from fastapi import APIRouter, Depends, Form, status, UploadFile, Query, File
from fastapi.responses import JSONResponse

from app.queries.news import add_news, get_news, news_list, news_list_by_interests, del_news
from app.user_hash import get_current_user

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


