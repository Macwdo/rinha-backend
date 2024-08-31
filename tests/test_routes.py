from fastapi.testclient import TestClient


def test_create_person_response_header(client: TestClient):
    response = client.post(
        "/pessoas",
        json={
            "nickname": "nickname",
            "name": "name",
            "birthdate": "2021-01-01",
            "stack": ["python", "fastapi"],
        },
    )
    assert response.status_code == 201
    assert response.headers["Location"] == "/pessoas/nickname"
