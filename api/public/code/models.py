from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

from api.utils.generic_models import UserCodeLink
from api.utils.generic_models import GameCodeLink
#from api.public.user.models import User
#from api.public.game.models import Game


class CodeBase(SQLModel):
    #name: str
    #headquarters: str
    remaining: int = None

    class Config:
        schema_extra = {
            "example": {
                #"name": "wonderful league",
                #"headquarters": "Fortress of Solitude",
                "remaining": 10,
            }
        }


class Code(CodeBase, table=True):
    # TODO randomize
    id: Optional[int] = Field(default=None, primary_key=True)

    # TODO users, games can have multiple access codes
    # but each access code should only be associated with one user, game pair
    users: List["User"] = Relationship(back_populates="codes", link_model=UserCodeLink)
    games: List["Game"] = Relationship(back_populates="codes", link_model=GameCodeLink)
    #user: "User" = Relationship(back_populates="codes", link_model=UserCodeLink)
    #game: "Game" = Relationship(back_populates="codes", link_model=GameCodeLink)


class CodeCreate(CodeBase):
    pass


class CodeRead(CodeBase):
    id: int
    #name: Optional[str] = None
    #headquarters: Optional[str] = None
    users: List = None
    games: List = None
    #user : "User" = None
    #game : "Game" = None
    remaining: int = None


class CodeUpdate(CodeBase):
    #name: Optional[str] = None
    #headquarters: Optional[str] = None
    remaining: int = None
