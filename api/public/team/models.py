from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

from api.utils.generic_models import UserTeamLink


class TeamBase(SQLModel):
    name: str
    headquarters: str

    class Config:
        schema_extra = {
            "example": {
                "name": "wonderful league",
                "headquarters": "Fortress of Solitude",
            }
        }


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    users: List["User"] = Relationship(back_populates="teams", link_model=UserTeamLink)


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int
    name: Optional[str] = None
    headquarters: Optional[str] = None
    users: List = None


class TeamUpdate(TeamBase):
    name: Optional[str] = None
    headquarters: Optional[str] = None
