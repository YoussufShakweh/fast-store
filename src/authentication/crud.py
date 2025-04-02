from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import get_password_hash

from .models import User
from .schemas import UserCreate, UserUpdate


async def get_users(*, db: AsyncSession, skip: int = 0, limit: int = 10) -> list[User]:
    stmt = select(User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user_by_id(*, db: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_user_by_email(*, db: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()


async def create_user(*, db: AsyncSession, user_in: UserCreate) -> User:
    user_data = user_in.model_dump(exclude_unset=True)
    password = user_data.pop("password")
    hashed_password = get_password_hash(password)

    db_user = User(**user_data, password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(*, db: AsyncSession, db_user: User, user_in: UserUpdate) -> User:
    user_data = user_in.model_dump(exclude_unset=True)

    if password := user_data.get("password"):
        user_data["password"] = get_password_hash(password)

    for attr, value in user_data.items():
        setattr(db_user, attr, value)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(*, db: AsyncSession, db_user: User) -> None:
    await db.delete(db_user)
    await db.commit()
