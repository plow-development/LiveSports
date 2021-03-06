from datetime import datetime, date

from fastapi import APIRouter, Form, status, File, Query
from fastapi.responses import JSONResponse

from app.models.models import EventOut, SportOut, EventComplex
from app.queries.events import add_event, events_list, events_list_by_datetime
from app.queries.sports import get_sport
from app.utils.utils import format_records, format_record

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


@router_events.get('/event/list', response_model=list[EventComplex])
async def List_of_events():
    list_events = await events_list()
    out = list()
    for event in list_events:
        out.append(EventComplex(
            event=format_record(event, EventOut),
            sport=format_record(await get_sport(event['sport_id']), SportOut)
        ))
    return out


@router_events.get('/event/list_by_datetime', response_model=list[EventComplex])
async def List_of_events_by_datetime(starttime: date = Query(..., description='Начало мероприятия')):
    list_events = await events_list_by_datetime(starttime)
    out = list()
    for event in list_events:
        out.append(EventComplex(
            event=format_record(event, EventOut),
            sport=format_record(await get_sport(event['sport_id']), SportOut)
        ))
    return out
