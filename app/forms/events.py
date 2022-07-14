from fastapi import APIRouter, Form, status, UploadFile, File
from fastapi.responses import JSONResponse
from datetime import datetime
from app.models.models import EventOut
from app.queries.events import add_event, events_list, events_list_by_datetime
from app.utils.utils import format_records

router_events = APIRouter(tags=['Мероприятия'])

@router_events.post('/event/create')
async def Creating_event(
        title: str = Form(..., description='Название мероприятия'),
        starttime: datetime = Form(..., description='Начало мероприятия'),
        latitude: float = File(..., description='Широта мероприятия'),
        longitude: float = Form(..., description='Долгота мероприятия')) -> JSONResponse:
    await add_event(title, starttime, latitude, longitude)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': f'Мероприятие «{title}» успешно добавлено!'})


@router_events.get('/event/list', response_model=list[EventOut])
async def List_of_events():
    return format_records(await events_list(), EventOut)


@router_events.post('/event/list', response_model=list[EventOut])
async def List_of_events_by_datetime(starttime: datetime = Form(..., description='Начало мероприятия')):
    return format_records(await events_list_by_datetime(starttime), EventOut)
