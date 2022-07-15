import asyncpg
from fastapi import APIRouter, Depends, Form, status, Query
from fastapi.responses import JSONResponse

from app.models.models import UserOut, TeamOut, SportOut, TeamComplex
from app.models.models import Created, Updated, Joined, Deleted
from app.queries.sports import get_sport
from app.queries.teams import team_add, team_get
from app.queries.users import get_user
from app.user_hash import get_current_user
from app.utils.utils import format_record

router_team = APIRouter(tags=['Команды участников'])


@router_team.post('/team/create', response_model=Created)
async def Create_team(
        user: asyncpg.Record = Depends(get_current_user),
        team_name: str = Form(..., description='Название команды'),
        sport_id: int = Form(..., description='ID вида спорта')):
    """
    Создание команды участников.  <br>
    Пользователь должен быть авторизован!  <br>
    """
    await team_add(team_name=team_name, user_id=user['user_id'], sport_id=sport_id)
    return Created()


@router_team.get('/team/get', response_model=TeamComplex)
async def Info_team(
        team_id: int = Query(..., description='ID команды')
) -> TeamComplex:
    """
    Выводит информацию о команде
    """
    team = (await team_get(team_id))['name']
    master_name = (await get_user(team['master_id']))['username']
    sport_name = (await get_sport(team['sport_id']))['name']

    return TeamComplex(
        team_name=format_record(team['name'], TeamOut),
        master_name=format_record(master_name, UserOut),
        sport_name=format_record(sport_name, SportOut)
    )
