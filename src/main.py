from datetime import date
from typing import Annotated
import redis
import asyncpg

from fastapi import FastAPI, Response, status
from pydantic import BaseModel, Field

import os

DATABASE = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", 5432),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", "postgres"),
    "database": os.environ.get("DB_NAME", "postgres"),
}

# `postgres://user:password@host:port/database?option=value
DB_DSN = f"postgres://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}"


class Database:
    def __init__(self, dsn):
        self._dsn = dsn

    async def connect(self):
        return await asyncpg.connect(dsn=self._dsn)


class Cache:
    def __init__(self, url):
        self._redis = redis.Redis.from_url(url)

    async def set(self, key, value):
        self._redis.set(key, value)

    async def get(self, key):
        return self._redis.get(key)


# cache = Cache(CACHE_URL)
# db = Database(DB_DSN)

app = FastAPI()


class Person(BaseModel):
    nickname: Annotated[str, Field(max_length=32)]
    name: Annotated[str, Field(max_length=100)]
    birthdate: date
    stack: list[Annotated[str, Field(max_length=32)]] | None


class PersonCreate(BaseModel):
    name: str
    birthdate: date
    stack: list[str] | None


@app.get("/pessoas")
async def people(t: str | None = None):
    return {}


@app.get("/pessoas/{person_id}")
async def person(person_id: int):
    return {}


@app.post("/pessoas")
async def create_person(person: Person):
    return Response(
        None,
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"/pessoas/{person.nickname}"},
    )


@app.get("/contagem-pessoas")
async def count_people():
    conn = await get_db()
    return {"time": conn}
