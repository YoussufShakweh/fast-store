from fastapi import FastAPI

from .authentication.routers.users import router as user_router
from .core.config import settings

app = FastAPI(root_path=settings.API_V1_STR)

app.include_router(user_router)
