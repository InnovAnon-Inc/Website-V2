from fastapi import APIRouter, Depends, Query
from pydantic.types import List
from sqlmodel import Session

from api.database import get_session
from api.public.user.crud import (
    create_user,
    delete_user,
    read_user,
    read_users,
    update_user,
)
from api.public.user.models import UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.post("", response_model=UserRead)
def create_a_user(user: UserCreate, db: Session = Depends(get_session)):
    return create_user(user=user, db=db)


@router.get("", response_model=List[UserRead])
def get_users(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    return read_users(offset=offset, limit=limit, db=db)


@router.get("/{user_id}", response_model=UserRead)
def get_a_user(user_id: int, db: Session = Depends(get_session)):
    return read_user(user_id=user_id, db=db)


@router.patch("/{user_id}", response_model=UserRead)
def update_a_user(user_id: int, user: UserUpdate, db: Session = Depends(get_session)):
    return update_user(user_id=user_id, user=user, db=db)


@router.delete("/{user_id}")
def delete_a_user(user_id: int, db: Session = Depends(get_session)):
    return delete_user(user_id=user_id, db=db)
