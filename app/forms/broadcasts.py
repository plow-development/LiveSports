from fastapi import APIRouter, Form, status, UploadFile, File
from fastapi.responses import JSONResponse

from app.models.models import BroadcastOut
from app.queries.broadcasts import add_broadcasts, broadcasts_list
from app.utils.utils import format_records

router_broadcasts = APIRouter(tags=['Прямые трансляции'])


@router_broadcasts.post('/broadcast/create')
async def Creating_broadcast(
        title: str = Form(..., description='Заголовок трансляции'),
        description: str = Form(..., description='Описание трансляции'),
        preview: UploadFile = File(..., description='Картинка трансляции'),
        link: str = Form(..., description='Ссылка на трансляцию')) -> JSONResponse:
    await add_broadcasts(title, description, preview, link)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': f'Трансляция «{title}» успешно добавлена!'})


@router_broadcasts.get('/broadcast/list', response_model=list[BroadcastOut])
async def List_of_broadcasts():
    return format_records(await broadcasts_list(), BroadcastOut)
