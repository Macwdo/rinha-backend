from datetime import date, datetime
from typing import Annotated
from fastapi import FastAPI, Response, status
from pydantic import BaseModel, Field


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
    pass
