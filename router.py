from typing import Annotated, Dict, Union

from fastapi import APIRouter, Depends

from repository import TaskRepository, NouUserRepository, \
                       RegistUserRepository, FitnessDataRepository
from schemas import STask, STaskADD, STaskGetByIdOne, STaskId, \
                    NounUsersPost, NounUsersOk, NounUsersGet, NounUsersGetId, \
                    UserRegisterPost, UserRegistOk, UserRegisterGet, \
                    UserRegId, RegUserUpdate, FitnessDataPost, \
                    FitnessDataGet, FitnessDataOk, FitnessDataId, \
                    FitnessDataUpdate

router = APIRouter(
    prefix='/tasks',
    tags=['Таски'],
)

router_users = APIRouter(
    prefix='/users',
    tags=['Аноним пользователи'],
)

router_regist_users = APIRouter(
    prefix='/regist',
    tags=['Зарегистрированные пользователи'],
)

router_fitness_data = APIRouter(
    prefix='/fitness_data',
    tags=['Фитнес данные'],
)

@router.post('')
async def add_tasks(
    task: Annotated[STaskADD, Depends()],
) -> Union[STaskId, Dict]:
    try:
        task_id = await TaskRepository.add_one(task)
        return {
            'ok': True, 'task_id': task_id
        }
    except Exception:
        return {
            'error': 'некорректные данные'
        }


@router.get('')
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.find_all()
    return tasks


@router.get('/{task_id}')
async def get_task_by_id(
    task: Annotated[STaskGetByIdOne, Depends()]
) -> Union[STaskId, Dict]:
    data = STaskGetByIdOne(id=task.id)
    task_schema = await TaskRepository.get_task_by_id(data)
    if task_schema:
        return STaskId(task_id=task_schema.id)
    else:
        # Обработка случая, когда объект не найден
        return {
            'error': 'такого объекта нет'
        }


@router.delete('')
async def delete_tasks(
    task: Annotated[STaskGetByIdOne, Depends()]
) -> Union[STaskId, Dict]:
    data = STaskGetByIdOne(id=task.id)
    task = await TaskRepository.delete_task_by_id(data)
    if task:
        return {
            'ok': task.id
        }
    return {
        'error': 'такого объекта нет'
    }


@router.patch('')
async def patch_tasks(
    task: Annotated[STask, Depends()],
) -> Union[STask, dict]:
    task = await TaskRepository.update_task(task)
    if task:
        return task
    return {
        'error': 'такого объекта нет'
    }


@router_users.post('/nouname_users')
async def add_nouname_users(
    noun_user: Annotated[NounUsersPost, Depends()],
) -> NounUsersOk:
    user_id = await NouUserRepository.add_one(noun_user)
    return {
        'ok': True, 'user_id': user_id
    }


@router_users.get('/nouname_users')
async def get_nouname_users() -> list[NounUsersGet]:
    users = await NouUserRepository.find_all()
    return users


@router_users.get('/{noun_user_id}')
async def get_user_noun_by_id(
    user: Annotated[NounUsersGetId, Depends()]
) -> Union[NounUsersGet, Dict]:
    data = NounUsersGetId(id=user.id)
    user_schema = await NouUserRepository.get_task_by_id(data)
    if user_schema:
        return NounUsersGet(
            id=user_schema.id, name=user_schema.name,
            telegram_id=user_schema.telegram_id,
            create_date=user_schema.create_date)
    else:
        # Обработка случая, когда объект не найден
        return {
            'error': 'такого объекта нет'
        }


@router_regist_users.post(
    '/add_user',
    description='Пароль должен быть больше 6 символов ' \
                'Имя должен быть больше 3 символов ' \
                'в почте должен быть "@"'
)
async def regist_add_user(
    task: Annotated[UserRegisterPost, Depends()],
) -> Union[UserRegistOk, Dict]:
    try:
        task_id = await RegistUserRepository.add_one(task)
        return {
            'ok': True, 'task_id': task_id
        }
    except Exception:  # Обработка других ошибок
        return {
            'error': 'Данные неправильно введены.'
        }



@router_regist_users.get('/get_users')
async def regist_users_get() -> list[UserRegisterGet]:
    tasks = await RegistUserRepository.find_all()
    return tasks


@router_regist_users.get('/{reg_user_id}')
async def get_user_reg_by_id(
    user: Annotated[UserRegId, Depends()]
) -> Union[UserRegisterGet, Dict]:
    data = UserRegId(id=user.id)
    user_schema = await RegistUserRepository.get_reg_user_by_id(data)
    if user_schema:
        return UserRegisterGet(
            id=user_schema.id, full_name=user_schema.full_name,
            telegram_id=user_schema.telegram_id,
            email=user_schema.email,
            create_date=user_schema.create_date,
            update_date=user_schema.update_date,)
    else:
        # Обработка случая, когда объект не найден
        return {
            'error': 'такого объекта нет'
        }


@router_regist_users.patch(
    '/update_reg_user',
    description='Пароль должен быть больше 6 символов ' \
                'Имя должен быть больше 3 символов ' \
                'в почте должен быть "@"'
    )
async def patch_reg_users(
    task: Annotated[RegUserUpdate, Depends()],
) -> Union[UserRegisterGet, dict]:
    task = await RegistUserRepository.update_user(task)
    if task:
        return task
    return {
            'error': 'Некорректные данные'
    }


@router_fitness_data.post('')
async def add_fitness_data(
    task: Annotated[FitnessDataPost, Depends()],
) -> Union[FitnessDataOk, Dict]:
    try:
        data_reg_user = await FitnessDataRepository.add_one(task)
        return {
            'ok': True, 'data_reg_user': [data_reg_user]
        }
    except Exception:
        return {
            'error': 'Некорректные данные'
            }


@router_fitness_data.get('/get_fitness_data_all_users')
async def fitness_data_users_get() -> list[FitnessDataGet]:
    tasks = await FitnessDataRepository.find_all()
    return tasks


@router_fitness_data.get('/{fitness_user_id}')
async def get_user_fitness_by_id(
    user: Annotated[FitnessDataId, Depends()]
):
    data = FitnessDataId(id=user.id)
    user_schema = await FitnessDataRepository.get_fitness_data_by_id(data)
    if user_schema:
        return FitnessDataGet(
            id=user_schema.id, weight=user_schema.weight,
            height=user_schema.height,
            age=user_schema.age,
            experience_years=user_schema.experience_years,
            experience_months=user_schema.experience_months,
            daily_activity=user_schema.daily_activity,
            focus_on_the_muscle_group=user_schema.focus_on_the_muscle_group,
            target=user_schema.target,
            registered_user_id=user_schema.registered_user_id,
            contraindications_health=user_schema.contraindications_health,
            create_date=user_schema.create_date,
            update_date=user_schema.update_date,)
    else:
        # Обработка случая, когда объект не найден
        return {
            'error': 'такого объекта нет'
        }


@router_fitness_data.patch(
    '/update_fitness_user',
    description='Пароль должен быть больше 6 символов ' \
                'Имя должен быть больше 3 символов ' \
                'в почте должен быть "@"'
    )
async def patch_fitness_users(
    task: Annotated[FitnessDataUpdate, Depends()],
) -> Union[FitnessDataGet, dict]:
    task = await FitnessDataRepository.update_fitness_user(task)
    if task:
        return task
    return {
        'error': 'Некорректные данные'
        }
