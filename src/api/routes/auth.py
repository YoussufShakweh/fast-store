from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.core.config import settings
from src.core.security import create_access_token
from src.deps import AsyncSessionDep
from src.schemas.token import Token
from src.services import user_services


router = APIRouter(tags=["Login"])


@router.post("/login", response_model=Token)
async def login(
    db: AsyncSessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = await user_services.authenticate(
        db=db, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=404, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(access_token=create_access_token(user.id, access_token_expires))
