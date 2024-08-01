from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator, \
                     validate_email

from sqlalchemy import BigInteger


class STaskGetByIdOne(BaseModel):
    id: int


class STaskADD(BaseModel):
    name: str
    description: Optional[str] = None
    registered_user_id: int

    @field_validator('name')
    def name_must_be_positive(cls, value):
        if len(value) < 1:
            raise ValueError('Имя должно быть длиннее 0')
        return value


class STask(STaskADD):
    id: int

    model_config = ConfigDict(from_attributes=True)


class STaskId(BaseModel):
    ok: bool = True
    task_id: int


class STaskDel(BaseModel):
    task_id: int


class NounUsersPost(BaseModel):
    name: str
    telegram_id: int

    model_config = ConfigDict(from_attributes=True)


class NounUsersGet(NounUsersPost):
    id: int
    create_date: datetime


class NounUsersGetId(BaseModel):
    id: int


class NounUsersOk(BaseModel):
    ok: bool = True
    user_id: int


class UserRegisterPost(BaseModel):
    full_name: str
    email: str
    password: str
    telegram_id: int

    @field_validator('password')
    def validate_password(cls, v: str) -> str:
        if len(v) > 5:
            return v
        return ValueError('Пароль должен быть больше 6 символов')


    @field_validator('full_name')
    def validate_full_name(cls, v: str) -> str:
        if len(v) > 3:
            return v
        return ValueError('Имя должен быть больше 6 символов')


    @field_validator('email')
    def validate_email_ad(cls, v: str) -> str:
        try:
            result = str(validate_email(v)[1])
            return result
        except Exception as error:
            return ValueError(f'неправильный емайл {error}')


class UserRegId(BaseModel):
    id: int


class UserRegisterGet(UserRegId):
    full_name: str
    email: str
    telegram_id: int
    create_date: datetime
    update_date: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdateGetPk(BaseModel):
    telegram_id: int


class UserRegistOk(UserRegId):
    ok: bool


class RegUserUpdate(UserRegId):
    full_name: str
    email: str
    telegram_id: int
    password: str

    @field_validator('password')
    def validate_password(cls, v: str) -> str:
        if len(v) > 5:
            return v
        return ValueError('Пароль должен быть больше 6 символов')

    @field_validator('full_name')
    def validate_full_name(cls, v: str) -> str:
        if len(v) > 3:
            return v
        return ValueError('Имя должен быть больше 6 символов')

    @field_validator('email')
    def validate_email_ad(cls, v: str) -> str:
        try:
            result = str(validate_email(v)[1])
            return result
        except Exception as error:
            return ValueError(f'неправильный емайл {error}')


class FitnessDataId(BaseModel):
    id: int


class FitnessDataPost(BaseModel):
    weight: int
    height: int
    age: int
    experience_years: int
    experience_months: int
    daily_activity: str
    registered_user_id: int
    focus_on_the_muscle_group: str
    target: Optional[str]
    contraindications_health: Optional[str]


class FitnessDataGet(FitnessDataPost, FitnessDataId):
    create_date: datetime
    update_date: datetime

    model_config = ConfigDict(from_attributes=True)


class FitnessDataOk(BaseModel):
    ok: bool
    data_reg_user: list


class FitnessDataUpdate(FitnessDataPost, FitnessDataId):
    pass
