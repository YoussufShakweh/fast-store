from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import func, select

from src.deps import AsyncSessionDep, CurrentUser, GetUserOr404
from src.models.user import User
from src.schemas.user import UserCreate, UserDetail, UserList, UserUpdate
from src.services import user_services


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=UserList)
async def read_users(
    db: AsyncSessionDep,
    q: str | None = None,
    is_active: bool | None = None,
    is_superuser: bool | None = None,
    skip: int = 0,
    limit: int = 10,
):
    conditions = []

    if q:
        conditions.append(User.email.icontains(q))

    if is_active is not None:
        conditions.append(User.is_active == is_active)

    if is_superuser is not None:
        conditions.append(User.is_superuser == is_superuser)

    count_stmt = select(func.count()).select_from(User)
    stmt = select(User).offset(skip).limit(limit)

    if conditions:
        count_stmt = count_stmt.where(*conditions)
        stmt = stmt.where(*conditions)

    count = (await db.execute(count_stmt)).scalar_one()
    users = (await db.execute(stmt)).scalars().all()

    return UserList(count=count, data=users)


@router.post("/", response_model=UserDetail, status_code=201)
async def create_user(form_data: UserCreate, db: AsyncSessionDep):
    user = await user_services.get_user_by_email(db=db, email=form_data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await user_services.create_user(db=db, user_in=form_data)


@router.get("/me", response_model=UserDetail)
async def read_user_me(current_user: CurrentUser):
    return current_user


@router.patch("/me", response_model=UserDetail)
async def update_user_me(
    current_user: CurrentUser, form_data: UserUpdate, db: AsyncSessionDep
):
    if form_data.email and form_data.email != current_user.email:
        existing_email = await user_services.get_user_by_email(
            db=db, email=form_data.email
        )
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
    current_user = await user_services.update_user(
        db=db, db_user=current_user, user_update=form_data
    )
    return current_user


@router.get("/{user_id}", response_model=UserDetail)
async def read_user(user: GetUserOr404):
    return user


@router.patch("/{user_id}", response_model=UserDetail)
async def update_user(user: GetUserOr404, form_data: UserUpdate, db: AsyncSessionDep):
    if form_data.email and form_data.email != user.email:
        existing_email = await user_services.get_user_by_email(
            db=db, email=form_data.email
        )
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
    user = await user_services.update_user(db=db, db_user=user, user_update=form_data)
    return user


@router.delete("/{user_id}", status_code=204)
async def delete_user(user: GetUserOr404, db: AsyncSessionDep):
    await user_services.delete_user(db=db, db_user=user)
    return Response(status_code=204)
