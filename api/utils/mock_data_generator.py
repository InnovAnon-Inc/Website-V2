from api.public.user.models import User
from api.public.team.models import Team
from api.database import engine
from sqlmodel import Session


def create_users_and_teams():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")
        wornderful_league = Team(
            name="Wonderful-League", headquarters="Fortress of Solitude"
        )

        user_deadpond = User(
            name="Deadpond",
            secret_name="Dive Wilson",
            age=24,
            teams=[team_z_force, team_preventers],
        )
        user_rusty_man = User(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            teams=[team_preventers],
        )
        user_spider_boy = User(
            name="Spider-Boy",
            secret_name="Pedro Parqueador",
            age=37,
            teams=[team_preventers],
        )
        user_super_good_boy = User(
            name="Super-Good-Boy",
            secret_name="John Goodman",
            age=30,
            teams=[wornderful_league, team_z_force],
        )

        session.add(user_deadpond)
        session.add(user_rusty_man)
        session.add(user_spider_boy)
        session.add(user_super_good_boy)
        session.commit()

        session.refresh(user_deadpond)
        session.refresh(user_rusty_man)
        session.refresh(user_spider_boy)
        session.refresh(user_super_good_boy)

        print("\n=========== MOCK DATA CREATED ===========\n")
        print("Deadpond:", user_deadpond)
        print("Deadpond teams:", user_deadpond.teams)
        print("Rusty-Man:", user_rusty_man)
        print("Rusty-Man Teams:", user_rusty_man.teams)
        print("Spider-Boy:", user_spider_boy)
        print("Spider-Boy Teams:", user_spider_boy.teams)
        print("Super-Good-Boy:", user_super_good_boy)
        print("Super-Good-Boy Teams:", user_super_good_boy.teams)
        print("\n===========================================\n")
