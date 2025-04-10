from typing import Annotated, AsyncGenerator
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import session
from src.models.user import User


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session() as db:
        try:
            yield db
        except Exception:
            await db.rollback()
            raise


AsyncSessionDep = Annotated[AsyncSession, Depends(get_db)]


async def get_user_or_404(user_id: UUID, db: AsyncSessionDep) -> User:
    db_user = await db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


GetUserOr404 = Annotated[User, Depends(get_user_or_404)]
