from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel

#from api.utils.generic_models import GameCodeLink
#from api.public.code.models import Code


class GameBase(SQLModel):
    name: str = Field(index=True)
    # TODO link to score and badge goals ?

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Flappy Bird",
                "code_id": 1,
            }
        }


class Game(GameBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    codes: List["Code"] = Relationship(back_populates="game")


class GameCreate(GameBase):
    pass


class GameRead(GameBase):
    id: int
    #codes: List = None


class GameUpdate(GameBase):
    name: Optional[str] = None
    codes: List = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Flappy Bird",
                "code_id": 1,
            }
        }
