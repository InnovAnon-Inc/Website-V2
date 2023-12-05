from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel

from api.public.team.models import Team
from api.public.code.models import Code
from api.public.badge.models import Badge
from api.utils.generic_models import UserTeamLink
from api.utils.generic_models import UserBadgeLink
from api.utils.generic_models import UserCodeLink


class UserBase(SQLModel):
    name: str
    secret_name: str
    age: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Super Man",
                "secret_name": "Clark Kent",
                "age": 27,
                "team_id": 1,
                "badge_id": 1,
                "number_invites": 2,
                "unclaimed_codes": 3,
            }
        }


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    teams: List[Team] = Relationship(back_populates="users", link_model=UserTeamLink)
    badges: List[Badge] = Relationship(back_populates="users", link_model=UserBadgeLink)
    codes: List[Code] = Relationship(back_populates="users", link_model=UserCodeLink)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    teams: List[Team] = None
    codes: List[Code] = None
    badges: List[Badge] = None
    number_invites: Optional[int] = None
    unclaimed_codes: Optional[int] = None


class UserUpdate(UserBase):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    teams: List[Team] = None
    codes: List[Code] = None
    badges: List[Badge] = None
    number_invites: Optional[int] = None
    unclaimed_codes: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Super Man",
                "secret_name": "Clark Kent",
                "age": 27,
                "team_id": 1,
                "badge_id": 1,
                "number_invites": 2,
                "unclaimed_codes": 3,
            }
        }
