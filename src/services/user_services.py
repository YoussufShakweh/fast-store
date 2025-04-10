from datetime import datetime, timezone
from sqlalchemy import select, update

from src.core.security import get_password_hash
from src.deps import AsyncSessionDep
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate


async def create_user(*, db: AsyncSessionDep, user_in: UserCreate) -> User:
    user_data = user_in.model_dump()
    password = user_data.pop("password")
    hashed_password = get_password_hash(password)
    db_user = User(**user_data, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_email(*, db: AsyncSessionDep, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().one_or_none()


async def update_user(
    *, db: AsyncSessionDep, user: User, user_update: UserUpdate
) -> User:
    user_data = user_update.model_dump(exclude_unset=True)
    stmt = update(User).where(User.id == user.id).values(**user_data)
    await db.execute(stmt)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(*, db: AsyncSessionDep, user: User) -> None:
    await db.delete(user)
    await db.commit()


async def update_last_login(*, db: AsyncSessionDep, user: User) -> User:
    stmt = (
        update(User)
        .where(User.id == user.id)
        .values(last_login=datetime.now(timezone.utc))
    )
    await db.execute(stmt)
    await db.commit()
    return user
