from functools import wraps
from sys import version as sysversion
from typing import ParamSpec
from typing import Any
from typing import List
from typing import TypeVar
from typing import Tuple
from typing import Dict
from typing import Callable
from typing import Union
from typing import Optional

from flask import Flask, request, jsonify
from typeguard import typechecked
from psycopg import connect
from psycopg import Connection
from psycopg import Cursor
from asyncpg import Pool
from asyncpg import create_pool
from asyncpg.pool import PoolConnectionProxy
from psycopg import ConnectionInfo
from psycopg import __version__ as dbversion
from asyncpg import __version__ as adbversion
from structlog import get_logger
from sqlfluff import lint

from ._version import version

T = TypeVar('T')
P = ParamSpec('P')

CallableVarArgs = Callable[P,T]
Wrapper         = Callable[[CallableVarArgs],CallableVarArgs]

SettingArg   = Tuple[str,...]
SettingKwArg = Dict[str,str]
CallableSettings = Callable[[SettingArg,SettingKwArg,P.args,P.kwargs],T]

CallablePool = Callable[[Pool,P.args,P.kwargs],T]
WrapperPool  = Callable[[CallablePool],CallablePool]

CallableConn = Callable[[Connection,P.args,P.kwargs],T]
WrapperConn  = Callable[[CallableConn],CallableConn]

CallableCurs = Callable[[Cursor,P.args,P.kwargs],T]
WrapperCurs  = Callable[[CallableCurs],CallableCurs]

CallableFlask = Callable[P, Flask]
CallableNone  = Callable[P,None]
WrapperFlask  = Callable[[CallableFlask, P.args, P.kwargs], CallableNone]

logger = get_logger()

@typechecked
def pgpool(func:CallablePool)->CallableSettings:
    @wraps(func)
    async def wrapper(pool_args:SettingArg, pool_kwargs:SettingKwArg, *args:P.args, **kwargs:P.kwargs)->T:
        pool:Pool = await create_pool(*pool_args, **pool_kwargs)
        try:
            return await func(pool, *args, **kwargs)
        finally:
            await pool.close()
    return wrapper

@typechecked
def pgconn(func:CallableConn)->CallablePool:
    @wraps(func)
    async def wrapper(pool:Pool, *args:P.args, **kwargs:P.kwargs)->T:
        async with pool.acquire() as conn:
            return await func(conn, *args, **kwargs)
    return wrapper

#@typechecked
#def pgcurs(func:CallableCurs)->CallableConn:
#    @wraps(func)
#    async def wrapper(conn:Connection, *args:P.args, **kwargs:P.kwargs)->T:
#        async with conn.cursor() as curs:
#            return await func(curs, *args, **kwargs)
#    return wrapper
#
#@typechecked
#def hellocurs(logger)->WrapperCurs:
#    @typechecked
#    def decorator(func:CallableCurs)->CallableCurs:
#        @wraps(func)
#        async def wrapper(curs:Cursor, *args:P.args, **kwargs:P.kwargs)->T:
#            await logger.ainfo('Cursor Name      : %s', curs.name)
#            await logger.ainfo('Cursor Scrollable: %s', curs.scrollable)
#            return await func(curs, *args, **kwargs)
#        return wrapper
#    return decorator

@typechecked
def helloconn(logger)->WrapperConn:
    @typechecked
    def decorator(func:CallableConn)->CallableConn:
        @wraps(func)
        async def wrapper(conn:Connection, *args:P.args, **kwargs:P.kwargs)->T:

            #from pprint import pprint
            #pprint(vars(conn))
            # TODO wtf
            #info:ConnectionInfo = conn.info
            #await logger.ainfo('Connection DSN: %s', info.dsn)

            return await func(conn, *args, **kwargs)
        return wrapper
    return decorator

@typechecked
def hellopool(logger)->WrapperPool:
    @typechecked
    def decorator(func:CallablePool)->CallablePool:
        @wraps(func)
        async def wrapper(pool:Pool, *args:P.args, **kwargs:P.kwargs)->T:
            await logger.ainfo('Pool Min     Size: %s', pool.get_min_size())
            await logger.ainfo('Pool Max     Size: %s', pool.get_max_size())
            await logger.ainfo('Pool Idle    Size: %s', pool.get_idle_size())
            await logger.ainfo('Pool Current Size: %s', pool.get_size())
            return await func(pool, *args, **kwargs)
        return wrapper
    return decorator

@typechecked
def hellopg(logger)->Wrapper:
    @typechecked
    def decorator(func:CallableVarArgs)->CallableVarArgs:
        @wraps(func)
        async def wrapper(*args:P.args, **kwargs:P.kwargs)->T:
            await logger.ainfo("psycopg %s", dbversion)
            await logger.ainfo("asyncpg %s", adbversion)
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@typechecked
def hellomain(logger)->Wrapper:
    @typechecked
    def decorator(func:CallableVarArgs)->CallableVarArgs:
        @wraps(func)
        async def wrapper(*args:P.args, **kwargs:P.kwargs)->T:
            await logger.ainfo("%s %s (c) 2023 Botze Co.", __name__, version)
            await logger.ainfo("Python %s", sysversion)
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@typechecked
def flask(func:CallableFlask, *flask_args:P.args, **flask_kwargs:P.kwargs)->WrapperFlask:
    async def wrapper(*args:P.args, **kwargs:P.kwargs)->None:
        app:Flask = await func(*args, **kwargs)
        return await app.run(*flask_args, **flask_kwargs)
    return wrapper

@typechecked
def sqlstr(q:str, dialect:str="postgres")->str:
    result:List[Dict[str,Union[str,int]]] = lint(q, dialect=dialect)
    assert not result, result
    return q









CREATE_TABLE_USER:str = sqlstr("""CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    invite_count INT NOT NULL DEFAULT 0,
    unclaimed_codes INT NOT NULL DEFAULT 0
)
""")
DROP_TABLE_USER:str = sqlstr("""DROP TABLE IF EXISTS "user"
""")

CREATE_TABLE_BADGE:str = sqlstr("""CREATE TABLE IF NOT EXISTS "badge" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
)
""")
DROP_TABLE_BADGE:str = sqlstr("""DROP TABLE IF EXISTS "badge"
""")

CREATE_TABLE_GAME:str = sqlstr("""CREATE TABLE IF NOT EXISTS "game" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
)
""")
DROP_TABLE_GAME:str = sqlstr("""DROP TABLE IF EXISTS "game"
""")

CREATE_TABLE_CODE:str = sqlstr("""CREATE TABLE IF NOT EXISTS "code" (
    id SERIAL PRIMARY KEY,
    secret VARCHAR(255) UNIQUE,
    remaining_uses INT NOT NULL DEFAULT 10,
    user_id INT NOT NULL REFERENCES "user" (id),
    game_id INT NOT NULL REFERENCES "game" (id),
    UNIQUE (user_id, game_id)
)
""")
DROP_TABLE_CODE:str = sqlstr("""DROP TABLE IF EXISTS "code"
""")

CREATE_TABLE_USERBADGELINK:str = sqlstr("""CREATE TABLE IF NOT EXISTS "userbadgelink" (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES "user" (id),
    badge_id INT NOT NULL REFERENCES "badge" (id),
    UNIQUE (user_id, badge_id)
)
""")
DROP_TABLE_USERBADGELINK:str = sqlstr("""DROP TABLE IF EXISTS "userbadgelink"
""")

@typechecked
async def create_table_user(conn:PoolConnectionProxy, *args:P.args, **kwargs:P.kwargs)->None:
    result:str = await conn.execute(CREATE_TABLE_USER)
    await logger.ainfo("create user table result: %s", result)
@typechecked
async def drop_table_user(conn:PoolConnectionProxy, *args:P.args, **kwargs:P.kwargs)->None:
    result:str = await conn.execute(DROP_TABLE_USER)
    await logger.ainfo("drop user table result: %s", result)

@typechecked
async def create_table_badge(conn:PoolConnectionProxy, *args:P.args, **kwargs:P.kwargs)->None:
    result:str = await conn.execute(CREATE_TABLE_BADGE)
    await logger.ainfo("create badge table result: %s", result)
@typechecked
async def drop_table_badge(conn:PoolConnectionProxy, *args:P.args, **kwargs:P.kwargs)->None:
    result:str = await conn.execute(DROP_TABLE_BADGE)
    await logger.ainfo("drop badge table result: %s", result)

@typechecked
async def create_table_game(conn:PoolConnectionProxy, *args:P.args, **kwargs:P.kwargs)->None:
    result:str = await conn.execute(CREATE_TABLE_GAME)
    await logger.ainfo("create game table result: %s", result)
@typechecked
async def drop_table_game(conn:PoolConnectionProxy, *args:P.args, **kwargs:P.kwargs)->None:
    result:str = await conn.execute(DROP_TABLE_GAME)
    await logger.ainfo("drop game table result: %s", result)

@typechecked
async def create_table_code(conn:PoolConnectionProxy, *args:P.args, **kwargs:P.kwargs)->None:
    result:str = await conn.execute(CREATE_TABLE_CODE)
    await logger.ainfo("create code table result: %s", result)
@typechecked
async def drop_table_code(conn:PoolConnectionProxy, *args:P.args, **kwargs:P.kwargs)->None:
    result:str = await conn.execute(DROP_TABLE_CODE)
    await logger.ainfo("drop code table result: %s", result)

@typechecked
async def create_table_userbadgelink(conn:PoolConnectionProxy, *args:P.args, **kwargs:P.kwargs)->None:
    result:str = await conn.execute(CREATE_TABLE_USERBADGELINK)
    await logger.ainfo("create userbadgelink table result: %s", result)
@typechecked
async def drop_table_userbadgelink(conn:PoolConnectionProxy, *args:P.args, **kwargs:P.kwargs)->None:
    result:str = await conn.execute(DROP_TABLE_USERBADGELINK)
    await logger.ainfo("drop userbadgelink table result: %s", result)

@pgconn
@helloconn(logger)
@typechecked
async def create_tables(conn:PoolConnectionProxy, *args:P.args, **kwargs:P.kwargs)->None:
    await create_table_user(conn)
    await create_table_badge(conn)
    await create_table_game(conn)
    await create_table_code(conn)
    await create_table_userbadgelink(conn)

@pgconn
@helloconn(logger)
@typechecked
async def drop_tables(conn:PoolConnectionProxy, *args:P.args, **kwargs:P.kwargs)->None:
    await drop_table_userbadgelink(conn)
    await drop_table_code(conn)
    await drop_table_game(conn)
    await drop_table_badge(conn)
    await drop_table_user(conn)

#####





SELECT_USERS:str = sqlstr("""SELECT
    id,
    name,
    invite_count,
    unclaimed_codes
FROM "user"
""")
SELECT_USER_BY_ID:str = (#sqlstr(
SELECT_USERS + """
WHERE id = %s
""")
SELECT_USER_BY_NAME:str = (#sqlstr(
SELECT_USERS + """
WHERE name = %s
""")


from itertools import starmap
from dataclasses import dataclass

@dataclass
class User:
    id:Optional[int]
    name:str
    invite_count:Optional[int]
    unclaimed_codes:Optional[int]

@pgconn
@typechecked
async def select_users(conn:PoolConnectionProxy, *args:P.args, **kwargs:P.kwargs)->List[User]:
    result:str = await conn.execute(SELECT_USERS)
    await logger.ainfo("select users result: %s", result)
    rows:List[Tuple[int,str,int,int]] = conn.fetchall()
    users:List[User] = list(starmap(User, rows))
    return users

@pgconn
@typechecked
async def select_user_by_id(conn:PoolConnectionProxy, user_id:int, *args:P.args, **kwargs:P.kwargs)->User:
    result:str = await conn.execute(SELECT_USER_BY_ID, user_id)
    await logger.ainfo("select user by id result: %s", result)
    row:Tuple[int,str,int,int] = conn.fetchone()
    user:User = User(*row)
    return user
    
@pgconn
@typechecked
async def select_user_by_name(conn:PoolConnectionProxy, name:str, *args:P.args, **kwargs:P.kwargs)->User:
    result:str = await conn.execute(SELECT_USER_BY_NAME, name)
    await logger.ainfo("select user by name result: %s", result)
    row:Tuple[int,str,int,int] = conn.fetchone()
    user:User = User(*row)
    return user

#INSERT_USER:str = (#sqlstr(
##"""INSERT INTO "user" VALUES (name) (?) RETURNING id
#"""INSERT INTO "user" (name)
#VALUES (%s)
#""")

@pgconn
@typechecked
async def create_user(conn:PoolConnectionProxy, user:User, *args:P.args, **kwargs:P.kwargs)->int:
    #conn.initialize(logger)
    await logger.adebug('INSERT_USER: %s', INSERT_USER)
    await logger.adebug('user: %s', user)
    #result:str = await conn.execute(INSERT_USER, (user.name,))
    result:str = await conn.execute("""INSERT INTO "user" (name) VALUES ("""+user.name+""")""")
    await logger.ainfo("create user result: %s", result)
    user_id:int = conn.fetchone()
    return user_id

# TODO update user

@pgconn
@typechecked
async def delete_user(conn:PoolConnectionProxy, user:User, *args:P.args, **kwargs:P.kwargs)->int:
    pass

@typechecked
async def create_app(pool:Pool)->Flask:
    app:Flask = Flask(__name__)

    @app.route('/users', methods=['GET'])
    async def get_users():
        #await logger.ainfo('foo: Hello, World!')
        #return await bar(pool, *args, **kwargs)
        pass

    # TODO create user
    # TODO get users
    # TODO get user
    # TODO update user
    # TODO delete user

    # TODO CRUD game
    # TODO CRUD badge
    # TODO CRUD code

    
    return app








#@pgconn
@typechecked
#async def test_user(conn:PoolConnectionProxy, *args:P.args, **kwargs:P.kwargs)->int:
async def test_user(conn:Pool, *args:P.args, **kwargs:P.kwargs)->int:
    user_name:str = "Flappy Player"
    user:User = User(None, user_name, None, None)
    user_id:int = await create_user(conn, user)

    user1:User = await select_user_by_id(conn, user_id)
    assert user == user1

    user2:User = await select_user_by_name(conn, user_name)
    assert user == user2

    users:List[User] = await select_users(conn)
    assert [user] == users

    delete_user(user_id)

    users2:List[User] = await select_users(conn)
    assert users2 == []




##########

@hellopg(logger)
@pgpool
@hellopool(logger)
@typechecked
async def helper(pool:Pool, flask_args:Tuple[Any,...], flask_kwargs:Dict[str,Any], *args:P.args, **kwargs:P.kwargs)->T:
    await create_tables(pool)
    #
    await test_user(pool)
    #
    app:CallableNone = flask(create_app, *flask_args, **flask_kwargs)
    return await app(pool, *args, **kwargs)

@hellomain(logger)
@typechecked
async def main(*args:P.args, **kwargs:P.kwargs)->T:
    pool_args   :SettingArg   = ()
    pool_kwargs :SettingKwArg = {}
    flask_args  :Tuple[Any,...]    = ()
    flask_kwargs:Dict[str,Any] = {
            "debug": True,
            "host": "0.0.0.0",
            #"port": 8000,
    }
    return await helper(pool_args, pool_kwargs, flask_args, flask_kwargs, *args, **kwargs)

