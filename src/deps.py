from typing import Annotated, AsyncGenerator
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.db.base import session
from src.models.user import User
from src.schemas.token import TokenPayload


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session() as db:
        try:
            yield db
        except Exception:
            await db.rollback()
            raise


AsyncSessionDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_user_or_404(user_id: UUID, db: AsyncSessionDep) -> User:
    db_user = await db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


GetUserOr404 = Annotated[User, Depends(get_user_or_404)]


async def get_current_user(db: AsyncSessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, [settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")

    user = await db.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
