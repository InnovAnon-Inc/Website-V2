from fastapi import APIRouter, Depends, Query
from pydantic.types import List
from sqlmodel import Session

from api.database import get_session
from api.public.badge.crud import (
    create_badge,
    delete_badge,
    read_badge,
    read_badges,
    update_badge,
)
from api.public.badge.models import BadgeCreate, BadgeRead, BadgeUpdate

router = APIRouter()


@router.post("", response_model=BadgeRead)
def create_a_badge(badge: BadgeCreate, db: Session = Depends(get_session)):
    return create_badge(badge=badge, db=db)


@router.get("", response_model=List[BadgeRead])
def get_badges(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    return read_badges(offset=offset, limit=limit, db=db)


@router.get("/{badge_id}", response_model=BadgeRead)
def get_a_badge(badge_id: int, db: Session = Depends(get_session)):
    return read_badge(badge_id=badge_id, db=db)


@router.patch("/{badge_id}", response_model=BadgeRead)
def update_a_badge(badge_id: int, badge: BadgeUpdate, db: Session = Depends(get_session)):
    return update_badge(badge_id=badge_id, badge=badge, db=db)


@router.delete("/{badge_id}")
def delete_a_badge(badge_id: int, db: Session = Depends(get_session)):
    return delete_badge(badge_id=badge_id, db=db)
