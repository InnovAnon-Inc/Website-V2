from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

from api.public.user.models import User
from api.public.game.models import Game


class CodeBase(SQLModel):
    secret: str = Field(index=True)
    remaining: Optional[int] = Field(default=None)
    user_id: Optional[int]  = Field(default=None, foreign_key="user.id")
    game_id: Optional[int]  = Field(default=None, foreign_key="game.id")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "secret": "abc123",
                "remaining": 10,
                "user_id": 1,
                "game_id": 1,
            }
        }


class Code(CodeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user:Optional[User] = Relationship(back_populates="codes")
    game:Optional[Game] = Relationship(back_populates="codes")


class CodeCreate(CodeBase):
    pass


class CodeRead(CodeBase):
    id: int
    #user: Optional[UserRead] = None
    #game: Optional[GameRead] = None


class CodeUpdate(CodeBase):
    remaining: Optional[int] = None
    secret:Optional[str] = None
    user_id: Optional[int] = None
    game_id: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "secret": "abc123",
                "remaining": 10,
                "user_id": 1,
                "game_id": 1,
            }
        }
