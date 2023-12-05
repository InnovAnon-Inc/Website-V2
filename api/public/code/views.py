from fastapi import APIRouter, Depends, Query
from pydantic.types import List
from sqlmodel import Session

from api.database import get_session
from api.public.code.crud import (
    create_code,
    delete_code,
    read_code,
    read_codes,
    update_code,
)
from api.public.code.models import CodeCreate, CodeRead, CodeUpdate

router = APIRouter()


@router.post("", response_model=CodeRead)
def create_a_code(code: CodeCreate, db: Session = Depends(get_session)):
    return create_code(code=code, db=db)


@router.get("", response_model=List[CodeRead])
def get_codes(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    return read_codes(offset=offset, limit=limit, db=db)


@router.get("/{code_id}", response_model=CodeRead)
def get_a_code(code_id: int, db: Session = Depends(get_session)):
    return read_code(code_id=code_id, db=db)


@router.patch("/{code_id}", response_model=CodeRead)
def update_a_code(code_id: int, code: CodeUpdate, db: Session = Depends(get_session)):
    return update_code(code_id=code_id, code=code, db=db)


@router.delete("/{code_id}")
def delete_a_code(code_id: int, db: Session = Depends(get_session)):
    return delete_code(code_id=code_id, db=db)
