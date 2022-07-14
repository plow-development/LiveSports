import asyncpg
from fastapi import APIRouter, Depends, Form, status, Query
from fastapi.responses import JSONResponse

from app.models.models import UserOut, TeamOut, SportOut, TeamComplex
from app.queries.sports import get_sport
from app.queries.teams import add_team, get_team
from app.queries.users import get_user
from app.user_hash import get_current_user
from app.utils.utils import format_record

router_team = APIRouter(tags=['Команды участников'])


@router_team.post('/team/add')
async def Create_team(
        team_name: str = Form(..., description='Название команды'),
        user_agent: asyncpg.Record = Depends(get_current_user),
        sport_id: int = Form(..., description='ID вида спорта')) -> JSONResponse:
    """
    Создание команды участников  <br>
    :param team_name: Название команды  <br>
    :param user_agent: Авторизованный пользователь  <br>
    :param sport_id: ID вида спорта  <br>
    """
    username = user_agent['username']
    user_id = await get_user_id(username)
    await add_team(team_name=team_name, user_id=user_id, sport_id=sport_id)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': f'Команда «{team_name}» успешно создана!'})


@router_team.get('/team/get', response_model=TeamComplex)
async def Info_team(
        team_id: int = Query(..., description='ID команды')) -> TeamComplexOut:
    """
    Выводит информацию о команде  <br>
    :param team_id: ID команды  <br>
    """
    team = (await get_team(team_id))['name']
    master_name = (await get_user(team['master_id']))['username']
    sport_name = (await get_sport(team['sport_id']))['name']

    return TeamComplex(
        team_name=format_record(team['name'], TeamOut),
        master_name=format_record(master_name, UserOut),
        sport_name=format_record(sport_name, SportOut)
    )
