from datetime import date, datetime

from pydantic import BaseModel, Field, EmailStr


class UserOut(BaseModel):
    user_id: int = Field(None, description='ID пользователя')
    username: str = Field(None, description='Псевдоним пользователя')
    email: EmailStr = Field(None, description='Почта пользователя')
    avatar: str = Field(None, description='Ссылка на аватар пользователя')
    firstname: str = Field(None, description='Имя пользователя')
    lastname: str = Field(None, description='Фамилия пользователя')
    birthday: date = Field(None, description='День Рожденья пользователя')
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


class NewsOut(BaseModel):
    news_id: int = Field(None, description='ID новости')
    title: str = Field(None, description='Заголовок новости')
    content: str = Field(None, description='Текст новости')
    preview: str = Field(None, description='Ссылка на превью новости')
    publictime: datetime = Field(None, description='Время публикации новости')
    author_id: int = Field(None, description='ID пользователя - автора новости')
    sport_id: int = Field(None, description='ID вида спорта, к которой относится новость')


class BroadcastOut(BaseModel):
    broadcast_id: int = Field(None, description='ID трансляции')
    title: str = Field(None, description='Заголовок трансляции')
    description: str = Field(None, description='Описание трансляции')
    preview: str = Field(None, description='Ссылка на превью трансляции')
    link: str = Field(None, description='Ссылка на трансляцию')


class EventOut(BaseModel):
    event_id: int = Field(None, description='ID мероприятия')
    name: str = Field(None, description='Название мероприятия')
    description: str = Field(None, description='Описание мероприятия')
    preview: str = Field(None, description='Ссылка на превью мероприятия')
    starttime: datetime = Field(None, description='Время начала мероприятия')
    latitude: float = Field(None, description='Широта местоположения мероприятия')
    longitude: float = Field(None, description='Долгота местоположения мероприятия')
    sport_id: int = Field(None, description='ID вида спорта, к которой относится мероприятие')


class UserComplex(BaseModel):
    user: UserOut = Field(None, description='Пользователь')
    teams: list[TeamOut] = Field(None, description='Команды, в которых состоит пользователь')
    sports: list[SportOut] = Field(None, description='Предпочитаемые виды спорта пользователя')


class TeamComplex(BaseModel):
    team: TeamOut = Field(None, description='Название команды')
    master_id: UserOut = Field(None, description='Владелец команды')
    sport: SportOut = Field(None, description='Вид спорта команды')
    users: UserOut = Field(None, description='Участники команды')


class NewsComplex(BaseModel):
    news: NewsOut = Field(None, description='Новость')
    author: UserOut = Field(None, description='Автор новости')
    sport: SportOut = Field(None, description='Вид спорта новости')


class Created(BaseModel):
    details: str = Field('Объект успешно создан!', title='Статус операции')


class Joined(BaseModel):
    details: str = Field('Добавление прошло успешно!', title='Статус операции')


class Deleted(BaseModel):
    details: str = Field('Удаление прошло успешно!', title='Статус операции')
