from datetime import date

from pydantic import BaseModel, Field, EmailStr


# UserOut

class BaseUserOut(BaseModel):
    username: str = Field(..., description='Ник пользователя')
    email: EmailStr = Field(..., description='Почта пользователя')
    avatar_url: str = Field(..., description='Аватарка пользователя')
    firstname: str = Field(..., description='Имя пользователя')
    lastname: str = Field(..., description='Фамилия пользователя')
    birthday: date = Field(..., description='День рожденья пользователя')
    money: int = Field(..., description='Баллы пользователя')


class UsersTeamOut(BaseModel):
    name: str = Field(None, description='Команда участников')


class BaseSportOut(BaseModel):
    name: str = Field(None, description='Вид спорта')


class UserComplex(BaseModel):
    user: BaseUserOut = Field(...)
    teams: list[UsersTeamOut] = Field(None)
    sport_types: list[BaseSportOut] = Field(None)


# UserOutInList

class BaseUserOutInList(BaseModel):
    username: str = Field(..., description='Ник пользователя')
    email: EmailStr = Field(..., description='Почта пользователя')
    avatar_url: str = Field(..., description='Аватарка пользователя')
    firstname: str = Field(..., description='Имя пользователя')
    lastname: str = Field(..., description='Фамилия пользователя')
    birthday: date = Field(..., description='День рожденья пользователя')
    money: int = Field(..., description='Баллы пользователя')


class UserComplexInList(BaseModel):
    user: BaseUserOutInList = Field(...)
    team: list[UsersTeamOut] = Field(None)
    sport_type: list[BaseSportOut] = Field(None)


# Sports

class SportsOut(BaseModel):
    name: str = Field(..., description='Название вида спорта')
    description: str = Field(..., description='Описание вида спорта')
    sport_type: str = Field(..., description='Тип вида спорта')

# Teams

class TeamNameOut(BaseModel):
    name: str = Field(None, description='Название команды')

class TeamUserNameOut(BaseModel):
    username: str = Field(None, description='Псевдоним владельца команды')

class TeamSportNameOut(BaseModel):
    name: str = Field(None, description='Вид спорта команды')

class TeamComplexOut(BaseModel):
    team_name: TeamNameOut = Field(None, description='Название команды')
    master_name: TeamUserNameOut = Field(None, description='Псевдоним владельца команды')
    sport_name: TeamSportNameOut = Field(None, description='Вид спорта команды')
