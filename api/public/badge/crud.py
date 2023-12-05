from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from api.database import get_session
from api.public.badge.models import Badge, BadgeCreate, BadgeUpdate


def create_badge(badge: BadgeCreate, db: Session = Depends(get_session)):
    badge_to_db = Badge.from_orm(badge)
    db.add(badge_to_db)
    db.commit()
    db.refresh(badge_to_db)
    return badge_to_db


def read_badges(offset: int = 0, limit: int = 20, db: Session = Depends(get_session)):
    badges = db.exec(select(Badge).offset(offset).limit(limit)).all()
    return badges


def read_badge(badge_id: int, db: Session = Depends(get_session)):
    badge = db.get(Badge, badge_id)
    if not badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Badge not found with id: {badge_id}",
        )
    return badge


def update_badge(badge_id: int, badge: BadgeUpdate, db: Session = Depends(get_session)):
    badge_to_update = db.get(Badge, badge_id)
    if not badge_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Badge not found with id: {badge_id}",
        )

    badge_data = badge.dict(exclude_unset=True)
    for key, value in badge_data.items():
        setattr(badge_to_update, key, value)

    db.add(badge_to_update)
    db.commit()
    db.refresh(badge_to_update)
    return badge_to_update


def delete_badge(badge_id: int, db: Session = Depends(get_session)):
    badge = db.get(Badge, badge_id)
    if not badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Badge not found with id: {badge_id}",
        )

    db.delete(badge)
    db.commit()
    return {"ok": True}
