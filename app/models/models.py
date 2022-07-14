from datetime import date

from pydantic import BaseModel, Field, EmailStr


class UserOut(BaseModel):
    user_id: int = Field(None, description='ID пользователя')
    username: str = Field(None, description='Ник пользователя')
    email: EmailStr = Field(None, description='Почта пользователя')
    avatar: str = Field(None, description='Аватарка пользователя')
    firstname: str = Field(None, description='Имя пользователя')
    lastname: str = Field(None, description='Фамилия пользователя')
    birthday: date = Field(None, description='День рожденья пользователя')
    money: int = Field(None, description='Баллы пользователя')


class SportOut(BaseModel):
    sport_id: int = Field(None, description='ID вида спорта')
    name: str = Field(None, description='Название вида спорта')
    description: str = Field(None, description='Описание вида спорта')
    sport_type: str = Field(None, description='Тип вида спорта')


class TeamOut(BaseModel):
    team_id: int = Field(None, description='ID команды')
    name: str = Field(None, description='Название команды')
    master_id: int = Field(None, description='ID пользователя - владельца команды')
    sport_id: int = Field(None, description='ID вида спорта команды')


class UserComplex(BaseModel):
    user: UserOut = Field(None, description='Участник')
    teams: list[TeamOut] = Field(None, description='Команды, в которых состоит участник')
    sports: list[SportOut] = Field(None, description='Предпочитаемые виды спорта')


class TeamComplex(BaseModel):
    team: TeamOut = Field(None, description='Название команды')
    master_id: UserOut = Field(None, description='Владелец команды')
    sport: SportOut = Field(None, description='Вид спорта команды')
    users: UserOut = Field(None, description='Участники команды')
