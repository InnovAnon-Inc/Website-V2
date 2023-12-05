from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel

#from api.public.code.models import Code
from api.utils.generic_models import UserBadgeLink
#from api.utils.generic_models import UserCodeLink
from api.public.badge.models import Badge


class UserBase(SQLModel):
    name           :str = Field(index=True)
    #number_invites :int = Field(default=0)
    #unclaimed_codes:int = Field(default=0)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Super Man",
                "number_invites": 2,
                "unclaimed_codes": 3,
                "badge_id": 1,
                "code_id": 1,
            }
        }


class User(UserBase, table=True):
    id    : Optional[int] = Field(default=None, primary_key=True)
    badges: List[Badge]   = Relationship(back_populates="users", link_model=UserBadgeLink)
    #codes : List[Code]    = Relationship(back_populates="users", link_model=UserCodeLink)
    #codes : List["Code"] = Relationship(back_populates="users")
    number_invites :int = Field(default=0)
    unclaimed_codes:int = Field(default=0)

    codes: List["Code"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    #name: Optional[str] = None
    number_invites: Optional[int] = None
    unclaimed_codes: Optional[int] = None
    #codes: List["Code"] = None
    badges: List[Badge] = None


class UserUpdate(UserBase):
    name: Optional[str] = None
    number_invites: Optional[int] = None
    unclaimed_codes: Optional[int] = None
    #codes: List["Code"] = None
    badges: List[Badge] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Super Man",
                "number_invites": 2,
                "unclaimed_codes": 3,
                "badge_id": 1,
                "code_id": 1,
            }
        }
