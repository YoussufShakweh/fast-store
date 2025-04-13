from fastapi import FastAPI

from src.api.routes.auth import router as auth_router
from src.api.routes.user import router as user_router
from src.core.config import settings


app = FastAPI(
    debug=settings.DEBUG,
    root_path=settings.API_V1_STR,
)

app.include_router(auth_router)
app.include_router(user_router)
