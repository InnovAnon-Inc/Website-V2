from typing import Optional
from sqlmodel import Field, SQLModel


class UserBadgeLink(SQLModel, table=True):
    badge_id: Optional[int] = Field(
        default=None, foreign_key="badge.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )

#class UserCodeLink(SQLModel, table=True):
#    code_id: Optional[int] = Field(
#        default=None, foreign_key="code.id", primary_key=True
#    )
#    user_id: Optional[int] = Field(
#        default=None, foreign_key="user.id", primary_key=True
#    )
#
#class GameCodeLink(SQLModel, table=True):
#    code_id: Optional[int] = Field(
#        default=None, foreign_key="code.id", primary_key=True
#    )
#    game_id: Optional[int] = Field(
#        default=None, foreign_key="game.id", primary_key=True
#    )
