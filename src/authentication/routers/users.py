from fastapi import APIRouter, HTTPException, status, Response
from src.core.deps import AsyncSessionDep

from .. import crud, schemas


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[schemas.UserList])
async def get_users(db: AsyncSessionDep, skip: int = 0, limit: int = 10):
    return await crud.get_users(db=db, skip=skip, limit=limit)


@router.post(
    "/", response_model=schemas.UserDetail, status_code=status.HTTP_201_CREATED
)
async def create_user(form_data: schemas.UserCreate, db: AsyncSessionDep):
    user = await crud.get_user_by_email(db=db, email=form_data.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    return await crud.create_user(db=db, user_in=form_data)


@router.get("/{user_id}", response_model=schemas.UserDetail)
async def get_user(user_id: int, db: AsyncSessionDep):
    user = await crud.get_user_by_id(db=db, user_id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


@router.patch("/{user_id}", response_model=schemas.UserDetail)
async def update_user(user_id: int, form_data: schemas.UserUpdate, db: AsyncSessionDep):
    db_user = await crud.get_user_by_id(db=db, user_id=user_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if form_data.email and form_data.email != db_user.email:
        existing_email = await crud.get_user_by_email(db=db, email=form_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    return await crud.update_user(db=db, db_user=db_user, user_in=form_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSessionDep):
    db_user = await crud.get_user_by_id(db=db, user_id=user_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    await crud.delete_user(db=db, db_user=db_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
