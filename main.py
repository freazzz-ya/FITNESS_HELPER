from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables, delete_tables
from router import router as tasks_touter
from router import router_users, router_regist_users, router_fitness_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    await create_tables()
    print("База готова")
    yield
    print("База очищена")

app = FastAPI(lifespan=lifespan)
app.include_router(router=tasks_touter)
app.include_router(router=router_users)
app.include_router(router=router_regist_users)
app.include_router(router=router_fitness_data)
