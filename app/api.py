from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.exceptions import CommonException
from app.services.database import DataBase
from app.forms.users import router_users
from app.forms.sports import router_sports
from app.forms.news import router_news

app = FastAPI(title='«Умный город: Живи спортом»')
static = StaticFiles(directory='resources/avatars')


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
app.include_router(router_news)

app.mount('/resources/avatars', static)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
