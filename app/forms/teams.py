import asyncpg
from fastapi import APIRouter, Depends, Form, status, Query
from fastapi.responses import JSONResponse

from app.models.models import UserOut, TeamOut, SportOut, TeamComplex
from app.models.models import Created, Updated, Joined, Deleted
from app.queries.sports import get_sport
from app.queries.teams import team_add, team_get, get_team_list_user
from app.queries.users import get_user, get_username
from app.user_hash import get_current_user
from app.utils.utils import format_record, format_records

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
    await get_sport(sport_id)
    await team_add(team_name=team_name, user_id=user['user_id'], sport_id=sport_id)
    return Created()


@router_team.get('/team/get', response_model=TeamComplex)
async def Team_Info(
        team_id: int = Query(..., description='ID команды')):
    """
    Выводит информацию о команде
    """
    team = await team_get(team_id)
    master_id = team['master_id']
    master = await get_user(await get_username(master_id))
    sport = await get_sport(team['sport_id'])
    users = await get_team_list_user(team_id)
    return TeamComplex(
        team=format_record(team, TeamOut),
        master=format_record(master, UserOut),
        sport=format_record(sport, SportOut),
        users=format_records(users, UserOut)
    )
