from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

from api.public.user.models import User
from api.public.game.models import Game


class CodeBase(SQLModel):
    remaining: int
    #user_id: int = Field(foreign_key="users.id")
    #game_id: int = Field(foreign_key="games.id")
    user_id: Optional[int]  = Field(default=None, foreign_key="user.id")
    game_id: Optional[int]  = Field(default=None, foreign_key="game.id")
    secret: str 

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "remaining": 10,
                #"user_id": 1,
                #"game_id": 1,
            }
        }


class Code(CodeBase, table=True):
    # TODO randomize
    id: Optional[int] = Field(default=None, primary_key=True)
    secret: Optional[str] = Field(default=None, primary_key=True)

    #user: "User" = Field(foreign_key="users.id")
    #game: "Game" = Field(foreign_key="games.id")
    # TODO
    #user: "User" = Relationship(back_populates="badges", link_model=UserBadgeLink)
    #user:"User" = Field(default=None, foreign_key="user.id")
    #game:"Game" = Field(default=None, foreign_key="game.id")
    user:Optional[User] = Relationship(back_populates="codes")
    game:Optional[Game] = Relationship(back_populates="codes")


class CodeCreate(CodeBase):
    pass


class CodeRead(CodeBase):
    id: int
    secret:str
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
                "remaining": 10,
                #"user_id": 1,
                #"game_id": 1,
            }
        }
