import pytest
from src.app import Person


@pytest.mark.parametrize(
    "data",
    [
        {
            "nickname": None,
            "name": "name",
            "birthdate": "2021-01-01",
            "stack": ["python", "fastapi"],
        },
        {
            "nickname": "nickname",
            "name": None,
            "birthdate": "2021-01-01",
            "stack": ["python", "fastapi"],
        },
        {
            "nickname": "nickname",
            "name": "name",
            "birthdate": None,
            "stack": ["python", "fastapi"],
        },
        {
            "nickname": "nickname",
            "name": "name",
            "birthdate": "2021-01-01",
            "stack": ["python", "bigger_than_32" * 5],
        },
        {
            "nickname": "nickname",
            "name": "name",
            "birthdate": "2021-01-01",
            "stack": ["python", 1],
        },
    ],
)
def test_person_invalid_fields(data):
    with pytest.raises(ValueError):
        Person(**data)
