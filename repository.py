from typing import Optional, Union

from sqlalchemy import delete, select

from database import TaskOrm, new_session, UsersGuests, RegisteredUser, \
                     FitnessData
from schemas import STask, STaskADD, STaskGetByIdOne, NounUsersGet, \
                    NounUsersPost, NounUsersOk, NounUsersGetId, \
                    UserRegisterPost, UserRegisterGet, UserRegistOk, \
                    UserRegId, RegUserUpdate, FitnessDataPost, FitnessDataGet, \
                    FitnessDataOk, FitnessDataId, FitnessDataUpdate


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskADD):
        async with new_session() as session:
            #  перевод в словарь
            task_dict = data.model_dump()
            task = TaskOrm(**task_dict)
            session.add(task)
            #  до коммита обновляет таск что присваивает ему id
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            # перевод к pydantic
            task_schemas = [
                STask.model_validate(task_model)
                for task_model in task_models
            ]
            return task_schemas

    @classmethod
    async def get_task_by_id(cls, data: STaskGetByIdOne) -> Optional[STask]:
        async with new_session() as session:
            query = select(TaskOrm).where(TaskOrm.id == data.id)
            result = await session.execute(query)
            task_model = result.scalars().first()
            if task_model:
                task_schema = STask.model_validate(task_model)
                return task_schema
            else:
                return None

    @classmethod
    async def delete_task_by_id(cls, data: STaskGetByIdOne) -> bool:
        async with new_session() as session:
            # Check if the task exists before attempting to delete
            query = select(TaskOrm).where(TaskOrm.id == data.id)
            result = await session.execute(query)
            task_model = result.scalars().first()

            if task_model:
                # Delete the task if it exists
                query = delete(TaskOrm).where(TaskOrm.id == data.id)
                await session.execute(query)
                await session.commit()
                return task_model  # Return True if deletion was successful
            else:
                return False  # Return False if the task doesn't exist

    @classmethod
    async def update_task(cls, data: STask) -> Union[STask, None]:
        async with new_session() as session:
            task = await session.get(TaskOrm, data.id)
            if not task:
                return False  # или raise exception
            #  обновляем атрибуты таска
            for key, value in data.model_dump().items():
                if key != 'id':
                    setattr(task, key, value)
            #  сохраняем изменения
            session.add(task)
            await session.commit()
            return STask.model_validate(task.__dict__)


class NouUserRepository:
    @classmethod
    async def find_all(cls) -> list[NounUsersGet]:
        async with new_session() as session:
            query = select(UsersGuests)
            result = await session.execute(query)
            user_nou_models = result.scalars().all()
            # перевод к pydantic
            task_schemas = [
                NounUsersGet.model_validate(task_model)
                for task_model in user_nou_models
            ]
            return task_schemas

    @classmethod
    async def add_one(cls, data: NounUsersPost):
        async with new_session() as session:
            #  перевод в словарь
            task_dict = data.model_dump()
            user = UsersGuests(**task_dict)
            session.add(user)
            #  до коммита обновляет таск что присваивает ему id
            await session.flush()
            await session.commit()
            return user.id

    @classmethod
    async def get_task_by_id(
        cls, data: NounUsersGetId
    ) -> Optional[NounUsersGet]:
        async with new_session() as session:
            query = select(UsersGuests).where(UsersGuests.id == data.id)
            result = await session.execute(query)
            task_model = result.scalars().first()
            if task_model:
                task_schema = NounUsersGet.model_validate(task_model)
                return task_schema
            else:
                return None


class RegistUserRepository:

    @classmethod
    async def add_one(cls, data: UserRegisterPost):
        async with new_session() as session:
            #  перевод в словарь
            task_dict = data.model_dump()
            user = RegisteredUser(**task_dict)
            session.add(user)
            #  до коммита обновляет таск что присваивает ему id
            await session.flush()
            await session.commit()
            return user.id

    @classmethod
    async def find_all(cls):
        async with new_session() as session:
            query = select(RegisteredUser)
            result = await session.execute(query)
            user_nou_models = result.scalars().all()
            # перевод к pydantic
            task_schemas = [
                UserRegisterGet.model_validate(task_model)
                for task_model in user_nou_models
            ]
            return task_schemas

    @classmethod
    async def get_reg_user_by_id(
        cls, data: UserRegId
    ) -> Optional[UserRegisterGet]:
        async with new_session() as session:
            query = select(RegisteredUser).where(RegisteredUser.id == data.id)
            result = await session.execute(query)
            task_model = result.scalars().first()
            if task_model:
                task_schema = UserRegisterGet.model_validate(task_model)
                return task_schema
            else:
                return None

    @classmethod
    async def update_user(
        cls, data: RegUserUpdate
    ) -> Union[UserRegisterGet, None]:
        async with new_session() as session:
            task = await session.get(RegisteredUser, data.id)
            if not task:
                return False  # или raise exception
            #  обновляем атрибуты таска
            for key, value in data.model_dump().items():
                if key != 'id':
                    setattr(task, key, value)
            #  сохраняем изменения
            session.add(task)
            await session.commit()
            return UserRegisterGet.model_validate(task.__dict__)


class FitnessDataRepository:
    @classmethod
    async def add_one(cls, data: FitnessDataPost):
        async with new_session() as session:
            #  перевод в словарь
            task_dict = data.model_dump()
            user = FitnessData(**task_dict)
            session.add(user)
            #  до коммита обновляет таск что присваивает ему id
            await session.flush()
            await session.commit()
            return FitnessDataPost(
                weight=user.weight,
                height=user.height, age=user.age,
                experience_years=user.experience_years,
                experience_months=user.experience_months,
                daily_activity=user.daily_activity,
                focus_on_the_muscle_group=user.focus_on_the_muscle_group,
                registered_user_id=user.registered_user_id,
                target=user.target,
                contraindications_health=user.contraindications_health,
            )

    @classmethod
    async def find_all(cls):
        async with new_session() as session:
            query = select(FitnessData)
            result = await session.execute(query)
            user_nou_models = result.scalars().all()
            # перевод к pydantic
            task_schemas = [
                FitnessDataGet.model_validate(task_model)
                for task_model in user_nou_models
            ]
            return task_schemas

    @classmethod
    async def get_fitness_data_by_id(
        cls, data: FitnessDataId
    ) -> Optional[FitnessDataGet]:
        async with new_session() as session:
            query = select(FitnessData).where(FitnessData.id == data.id)
            result = await session.execute(query)
            task_model = result.scalars().first()
            if task_model:
                task_schema = FitnessDataGet.model_validate(task_model)
                return task_schema
            else:
                return None

    @classmethod
    async def update_fitness_user(
            cls, data: FitnessDataUpdate
        ) -> Union[FitnessDataGet, None]:
        async with new_session() as session:
            task = await session.get(FitnessData, data.id)
            if not task:
                return None  # или raise exception
            #  обновляем атрибуты таска
            for key, value in data.model_dump().items():
                if key != 'id':
                    setattr(task, key, value)
            try:
                #  сохраняем изменения
                session.add(task)
                await session.commit()
            except Exception:
                return None  # Возвращаем None при ошибке целостности данных
            return FitnessDataGet.model_validate(task.__dict__) 
