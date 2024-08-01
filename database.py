from typing import Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn, mapped_column
from sqlalchemy import func, ForeignKey, Integer, UniqueConstraint, \
                        ForeignKeyConstraint,  PrimaryKeyConstraint, Index, \
                        Column, BigInteger
from sqlalchemy.orm import relationship


DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'FAST_API_DB'
DB_USER = 'home'
DB_PASSWORD = '11w11w'


DATABASE_URL = f'postgresql+asyncpg:' \
               f'//{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


engine = create_async_engine(DATABASE_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class RegisteredUser(Model):
    __tablename__ = "register_users"

    id: Mapped[int] = MappedColumn(primary_key=True)
    telegram_id: Mapped[int] = MappedColumn(BigInteger)
    full_name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    create_date: Mapped[datetime] = MappedColumn(insert_default=func.now())
    update_date: Mapped[datetime] = MappedColumn(
        default=datetime.now, onupdate=datetime.now
    )

    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_pk'),
        UniqueConstraint('telegram_id'),
        UniqueConstraint('email'),
    )


class TaskOrm(Model):
    __tablename__ = "tasks"

    id: Mapped[int] = MappedColumn(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    registered_user_id: Mapped[int] = MappedColumn(
        foreign_key="register_users.id"
    )

    __table_args__ = (
        ForeignKeyConstraint(['registered_user_id'], ['register_users.id']),         
    )


class UsersGuests(Model):
    __tablename__ = "usersguests"

    id: Mapped[int] = MappedColumn(primary_key=True)
    name: Mapped[str]
    telegram_id: Mapped[int]
    create_date: Mapped[datetime] = MappedColumn(insert_default=func.now())


class FitnessData(Model):
    __tablename__ = "fitness_data"

    id: Mapped[int] = MappedColumn(primary_key=True)
    weight: Mapped[int]
    height: Mapped[int]
    age: Mapped[int]
    experience_years: Mapped[int]  # Годы
    experience_months: Mapped[int] 
    daily_activity: Mapped[str]
    focus_on_the_muscle_group: Mapped[str]
    target: Mapped[Optional[str]]
    contraindications_health: Mapped[Optional[str]]
    registered_user_id: Mapped[int] = MappedColumn(
        foreign_key="register_users.id", unique=True
    )
    create_date: Mapped[datetime] = MappedColumn(insert_default=func.now())
    update_date: Mapped[datetime] = MappedColumn(
        default=datetime.now, onupdate=datetime.now
    )

    __table_args__ = (
        ForeignKeyConstraint(['registered_user_id'], ['register_users.id']),
        PrimaryKeyConstraint('id', name='fitness_pk'),
    )


#  создание таблиц
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


# удаление таблиц
async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
