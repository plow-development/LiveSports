from fastapi import APIRouter, Form, status, Query
from fastapi.responses import JSONResponse

from app.models.models import SportOut
from app.queries.sports import add_sport, get_sport, get_sport_id, get_list_sport, edit_sport_name, edit_sport_description, edit_sport_type
from app.utils.utils import format_record, format_records

router_sports = APIRouter(tags=['Виды спорта'])


@router_sports.post('/sport')
async def Creating_a_sport(
        sport_name: str = Form(..., description='Название вида спорта'),
        description: str = Form(..., description='Описание вида спорта'),
        sport_type: str = Form(..., description='Тип вида спорта')
) -> JSONResponse:
    """
    Создание вида спорта

    :param sport_name: Название вида спорта<br>
    :param description: Описание вида спорта<br>
    :param sport_type: Тип вида спорта<br>
    :return: JSONResponse HTTP_201_CREATED
    """
    await add_sport(name=sport_name, description=description, sport_type=sport_type)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': f'Вид спорта «{sport_name}» успешно создан!'})


@router_sports.post('/sport/edit/name')
async def Edit_Sport_Name(
        sport_id: int = Form(..., description='ID вида спорта'),
        sport_name: str = Form(..., description='Название вида спорта')):
    await edit_sport_name(sport_id=sport_id, name=sport_name)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={'message': 'Вид спорта успешно переименован!'})


@router_sports.post('/sport/edit/type')
async def Edit_Sport_Type(
        sport_id: int = Form(..., description='ID вида спорта'),
        sport_type: str = Form(..., description='Тип вида спорта')):
    await edit_sport_type(sport_id=sport_id, sport_type=sport_type)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={'message': 'Тип вида спорта успешно переименован!'})


@router_sports.get('/sport/get', response_model=SportOut)
async def Information_about_the_sport(
        sport_name: str = Query(..., description='Название вида спорта')) -> SportOut | None:
    """
    :param sport_name: Название вида спорта<br>
    :return: Информация о виде спорта
    """
    sport_id: int = await get_sport_id(sport_name)
    return format_record(await get_sport(sport_id), SportOut)


@router_sports.get('/sport/list', response_model=list[SportOut])
async def List_of_sports() -> list:
    """
    :return: Список видов спорта
    """
    list_sports = await get_list_sport()
    return format_records(list_sports, SportOut)
