from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.exceptions import CommonException
from app.services.database import DataBase
from app.forms.users import router_users
from app.forms.sports import router_sports
from app.forms.teams import router_team
from app.forms.news import router_news
from app.forms.broadcasts import router_broadcasts
from app.forms.events import router_events

app = FastAPI(title='«Умный город: Живи спортом»')


@app.on_event('startup')
async def startup() -> None:
    await DataBase.connect_db()


@app.on_event('shutdown')
async def shutdown() -> None:
    await DataBase.disconnect_db()


@app.exception_handler(CommonException)
async def handler_badrequest(requests: Request, exception: CommonException) -> JSONResponse:
    return JSONResponse(status_code=exception.code, content={'details': exception.message})


app.include_router(router_users)
app.include_router(router_sports)
app.include_router(router_team)
app.include_router(router_news)
app.include_router(router_broadcasts)
app.include_router(router_events)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
