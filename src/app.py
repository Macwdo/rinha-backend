from contextlib import asynccontextmanager
import json
import uuid
from dotenv import load_dotenv
import redis
import asyncpg

from fastapi import Depends, FastAPI, Response, status, APIRouter

import os

import redis.asyncio

from src.models import Person, PersonCreate, PersonDetail

load_dotenv()

REDIS_DSN = os.environ.get("REDIS_DSN", "redis://localhost:6379/")
DB_DSN = os.environ.get("DB_DSN", "postgresql://user:password@localhost/postgres")


class Database:
    def __init__(self, dsn):
        self._dsn = dsn

    async def connect(self):
        if hasattr(self, "_con"):
            return self._con

        con = await asyncpg.connect(dsn=self._dsn)
        self._con = con
        return con

    async def fetch(self, query, *args):
        return await self._con.fetch(query, *args)

    async def execute(self, query, *args):
        return await self._con.execute(query, *args)

    async def run_script(self):
        with open("./ddl.sql", "r") as f:
            script = f.read().replace("\n", " ")

        return await self._con.execute(script)


class Cache:
    def __init__(self, dsn):
        self._dsn = dsn

    def connect(self):
        if hasattr(self, "_redis"):
            return self._redis

        self._redis = redis.asyncio.Redis.from_url(url=self._dsn)
        return self._redis

    async def set(self, key, value):
        self._redis.set(key, value)

    async def get(self, key, optional_result=None):
        return await self._redis.get(key) or optional_result


db = Database(DB_DSN)
cache = Cache(REDIS_DSN)


def get_db():
    return app.state.db


def get_cache():
    return app.state.cache


async def setup_app():
    await db.connect()
    await db.run_script()
    await cache.connect()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_app()

    app.state.db = db
    app.state.cache = cache
    yield


app = FastAPI(lifespan=lifespan)

hc = APIRouter(prefix="/health-check", tags=["health-check"])


@hc.get("/")
def health_check():
    return {"status": "ok"}


@hc.get("/db")
async def hc_db(db: Database = Depends(get_db)):
    now = await db.fetch("SELECT NOW() AS now")
    return {"status": "ok", "now": now[0]["now"]}


@hc.get("/cache")
async def hc_cache(cache: Cache = Depends(get_cache)):
    ping = await cache.get("ping")
    return {"ping": ping}


app.include_router(hc)


@app.get("/pessoas")
# TODO: Add t search parameter
async def people(t: str | None = None):
    people = await db.fetch("SELECT * FROM pessoas")
    people = [
        PersonDetail(
            id=person["id"],
            nickname=person["apelido"],
            name=person["nome"],
            birthdate=person["data_nascimento"],
            stack=person["stack"],
        )
        for person in people
    ]
    return people


@app.get("/pessoas/{person_id}")
async def person(person_id: uuid.UUID):
    person = await db.fetch("SELECT * FROM pessoas WHERE id = $1", person_id)

    return PersonDetail(
        id=person[0]["id"],
        nickname=person[0]["apelido"],
        name=person[0]["nome"],
        birthdate=person[0]["data_nascimento"],
        stack=person[0]["stack"],
    )


@app.post("/pessoas")
async def create_person(person: Person):
    try:
        query = "INSERT INTO pessoas (id, apelido, nome, data_nascimento, stack) VALUES ($1, $2, $3, $4, $5)"
        generated_id = uuid.uuid4()
        await db.execute(
            query,
            generated_id,
            person.nickname,
            person.name,
            person.birthdate,
            json.dumps(person.stack),
        )

    except asyncpg.exceptions.UniqueViolationError:
        return Response(None, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    return Response(
        None,
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"/pessoas/{generated_id}"},
    )


@app.get("/contagem-pessoas")
async def count_people(): ...
