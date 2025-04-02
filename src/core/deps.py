from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .database import session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session() as db:
        try:
            yield db
        except Exception:
            await db.rollback()
            raise


AsyncSessionDep = Annotated[AsyncSession, Depends(get_db)]
