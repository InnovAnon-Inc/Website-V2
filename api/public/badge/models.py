from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

from api.utils.generic_models import UserBadgeLink


class BadgeBase(SQLModel):
    name: str
    #headquarters: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Flight 69",
                #"headquarters": "Fortress of Solitude",
            }
        }


class Badge(BadgeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    users: List["User"] = Relationship(back_populates="badges", link_model=UserBadgeLink)


class BadgeCreate(BadgeBase):
    pass


class BadgeRead(BadgeBase):
    id: int
    name: Optional[str] = None
    #headquarters: Optional[str] = None
    users: List = None


class BadgeUpdate(BadgeBase):
    name: Optional[str] = None
    #headquarters: Optional[str] = None
