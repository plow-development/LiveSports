from fastapi import APIRouter, Form, status
from fastapi.responses import JSONResponse

from app.models.models import BaseSportOut
from app.queries.sports import add_sport, get_sport_id, get_sport_name, get_list_sport
from app.utils.utils import format_record, format_records

router_sports = APIRouter(tags=['Виды спорта'])


@router_sports.post('/sport')
async def Creating_a_sport(
        name: str = Form(..., description='Название вида спорта'),
        description: str = Form(..., description='Описание вида спорта'),
        sport_type: str = Form(..., description='Тип вида спорта')
) -> JSONResponse:
    """
    Создание вида спорта

    :param name: Название вида спорта
    :param description: Описание вида спорта
    :param sport_type: Тип вида спорта
    :return: JSONResponse HTTP_201_CREATED
    """
    await add_sport(name=name, description=description, sport_type=sport_type)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': f'Вид спорта «{name}» успешно создан!'})

