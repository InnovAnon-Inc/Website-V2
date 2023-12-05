from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from api.database import get_session
from api.public.code.models import Code, CodeCreate, CodeUpdate


def create_code(code: CodeCreate, db: Session = Depends(get_session)):
    code_to_db = Code.from_orm(code)
    db.add(code_to_db)
    db.commit()
    db.refresh(code_to_db)
    return code_to_db


def read_codes(offset: int = 0, limit: int = 20, db: Session = Depends(get_session)):
    codes = db.exec(select(Code).offset(offset).limit(limit)).all()
    return codes


def read_code(code_id: int, db: Session = Depends(get_session)):
    code = db.get(Code, code_id)
    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Code not found with id: {code_id}",
        )
    return code


def update_code(code_id: int, code: CodeUpdate, db: Session = Depends(get_session)):
    code_to_update = db.get(Code, code_id)
    if not code_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Code not found with id: {code_id}",
        )

    code_data = code.dict(exclude_unset=True)
    for key, value in code_data.items():
        setattr(code_to_update, key, value)

    db.add(code_to_update)
    db.commit()
    db.refresh(code_to_update)
    return code_to_update


def delete_code(code_id: int, db: Session = Depends(get_session)):
    code = db.get(Code, code_id)
    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Code not found with id: {code_id}",
        )

    db.delete(code)
    db.commit()
    return {"ok": True}
