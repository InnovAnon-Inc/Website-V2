from fastapi import APIRouter, Depends, Query
from pydantic.types import List
from sqlmodel import Session

from api.database import get_session
from api.public.game.crud import (
    create_game,
    delete_game,
    read_game,
    read_games,
    update_game,
)
from api.public.game.models import GameCreate, GameRead, GameUpdate

router = APIRouter()


@router.post("", response_model=GameRead)
def create_a_game(game: GameCreate, db: Session = Depends(get_session)):
    return create_game(game=game, db=db)


@router.get("", response_model=List[GameRead])
def get_games(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    return read_games(offset=offset, limit=limit, db=db)


@router.get("/{game_id}", response_model=GameRead)
def get_a_game(game_id: int, db: Session = Depends(get_session)):
    return read_game(game_id=game_id, db=db)


@router.patch("/{game_id}", response_model=GameRead)
def update_a_game(game_id: int, game: GameUpdate, db: Session = Depends(get_session)):
    return update_game(game_id=game_id, game=game, db=db)


@router.delete("/{game_id}")
def delete_a_game(game_id: int, db: Session = Depends(get_session)):
    return delete_game(game_id=game_id, db=db)
