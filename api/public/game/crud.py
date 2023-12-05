from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from api.database import get_session
from api.public.game.models import Game, GameCreate, GameUpdate


def create_game(game: GameCreate, db: Session = Depends(get_session)):
    game_to_db = Game.from_orm(game)
    db.add(game_to_db)
    db.commit()
    db.refresh(game_to_db)
    return game_to_db


def read_games(offset: int = 0, limit: int = 20, db: Session = Depends(get_session)):
    games = db.exec(select(Game).offset(offset).limit(limit)).all()
    return games


def read_game(game_id: int, db: Session = Depends(get_session)):
    game = db.get(Game, game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game not found with id: {game_id}",
        )
    return game


def update_game(game_id: int, game: GameUpdate, db: Session = Depends(get_session)):
    game_to_update = db.get(Game, game_id)
    if not game_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game not found with id: {game_id}",
        )

    team_data = game.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(game_to_update, key, value)

    db.add(game_to_update)
    db.commit()
    db.refresh(game_to_update)
    return game_to_update


def delete_game(game_id: int, db: Session = Depends(get_session)):
    game = db.get(Game, game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game not found with id: {game_id}",
        )

    db.delete(game)
    db.commit()
    return {"ok": True}
