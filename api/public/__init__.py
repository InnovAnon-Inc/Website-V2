from fastapi import APIRouter

from api.public.user import views as users
from api.public.team import views as teams
from api.public.game import views as games
from api.public.badge import views as badges
from api.public.code import views as codes

api = APIRouter()


api.include_router(users.router, prefix="/users", tags=["Users"])
api.include_router(teams.router, prefix="/teams", tags=["Teams"])
api.include_router(games.router, prefix="/games", tags=["Games"])
api.include_router(badges.router, prefix="/badges", tags=["Badges"])
api.include_router(codes.router, prefix="/codes", tags=["Codes"])
