from fastapi import APIRouter

from api.public.user import views as users
from api.public.team import views as teams

api = APIRouter()


api.include_router(users.router, prefix="/users", tags=["Users"])
api.include_router(teams.router, prefix="/teams", tags=["Teams"])
