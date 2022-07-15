from datetime import datetime, date

from fastapi import APIRouter, Form, status, File, Query
from fastapi.responses import JSONResponse

from app.models.models import EventOut
from app.queries.events import add_event, events_list, events_list_by_datetime
from app.utils.utils import format_records

router_events = APIRouter(tags=['Мероприятия'])

@router_events.post('/event/create')
async def Creating_event(
        name: str = Form(..., description='Название мероприятия'),
        description: str = Form(..., description='Описание мероприятия'),
        preview: str = Form(..., description='Превью мероприятия'),
        starttime: datetime = Form(..., description='Начало мероприятия'),
        latitude: float = File(..., description='Широта местоположения мероприятия'),
        longitude: float = Form(..., description='Долгота местоположения мероприятия'),
        sport_id: int = File(..., description='ID вида спорта')) -> JSONResponse:
    await add_event(name, description, preview, starttime, latitude, longitude, sport_id)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': f'Мероприятие «{name}» успешно добавлено!'})


@router_events.get('/event/list', response_model=list[EventOut])
async def List_of_events():
    return format_records(await events_list(), EventOut)


@router_events.get('/event/list_by', response_model=list[EventOut])
async def List_of_events_by_datetime(starttime: date = Query(..., description='Начало мероприятия')):
    return format_records(await events_list_by_datetime(starttime), EventOut)
