from datetime import date

from pydantic import BaseModel, Field, EmailStr

# UserOut

class BaseUserOut(BaseModel):
    username: str = Field(..., description='Ник пользователя')
    email: EmailStr = Field(None, description='Почта пользователя')
    avatar_url: str = Field(None, description='Аватарка пользователя')
    firstname: str = Field(None, description='Имя пользователя')
    lastname: str = Field(None, description='Фамилия пользователя')
    birthday: date = Field(None, description='День рожденья пользователя')
    type_: str = Field(None, description='Тип пользователя')
    money: int = Field(None, description='Баллы пользователя')

class BaseTeamOut(BaseModel):
    name: str = Field(None, description='Команда участников')

class BaseSportOut(BaseModel):
    name: str = Field(None, description='Вид спорта')

class UserComplex(BaseModel):
    user: BaseUserOut = Field(...)
    teams: list[BaseTeamOut] = Field(None)
    sport_types: list[BaseSportOut] = Field(None)

# UserOutInList

class BaseUserOutInList(BaseModel):
    username: str = Field(..., description='Ник пользователя')
    email: EmailStr = Field(..., description='Почта пользователя')
    avatar_url: str = Field(..., description='Аватарка пользователя')
    firstname: str = Field(..., description='Имя пользователя')
    lastname: str = Field(..., description='Фамилия пользователя')
    birthday: date = Field(..., description='День рожденья пользователя')
    type_: str = Field(..., description='Тип пользователя')
    money: int = Field(..., description='Баллы пользователя')

class UserComplexInList(BaseModel):
    user: BaseUserOutInList = Field(...)
    team: list[BaseTeamOut] = Field(None)
    sport_type: list[BaseSportOut] = Field(None)
