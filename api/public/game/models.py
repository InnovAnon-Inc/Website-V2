from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel

from api.public.code.models import Code
from api.utils.generic_models import GameCodeLink


class GameBase(SQLModel):
    name: str
    #secret_name: str
    #age: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Flappy Bird",
                #"secret_name": "Clark Kent",
                #"age": 27,
                "code_id": 12345,
            }
        }


class Game(GameBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    codes: List[Code] = Relationship(back_populates="games", link_model=GameCodeLink)


class GameCreate(GameBase):
    pass


class GameRead(GameBase):
    id: int
    name: Optional[str] = None
    #secret_name: Optional[str] = None
    #age: Optional[int] = None
    #codes: List[Code] = None


class GameUpdate(GameBase):
    name: Optional[str] = None
    #secret_name: Optional[str] = None
    #age: Optional[int] = None
    #codes: List[Code] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Flappy Bird",
                #"secret_name": "Clark Kent",
                #"age": 27,
                "code_id": 12345,
            }
        }
