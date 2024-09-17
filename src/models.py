from datetime import date
from json import loads
from typing import Annotated
import uuid
from pydantic import BaseModel, Field, field_validator, validator


class Person(BaseModel):
    nickname: Annotated[str, Field(max_length=32)]
    name: Annotated[str, Field(max_length=100)]
    birthdate: date
    stack: list[Annotated[str, Field(max_length=32)]] | None


class PersonCreate(Person):
    id: uuid.UUID


class PersonDetail(Person):
    id: uuid.UUID

    @field_validator("stack", mode="before")
    @classmethod
    def validate_stack(cls, v):
        if isinstance(v, str):
            return loads(v)

        return v
