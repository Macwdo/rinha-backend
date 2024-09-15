FROM python:3.12

ENV POETRY_VIRTUALENVS_CREATE=false
WORKDIR /code

COPY pyproject.toml poetry.lock /code/
COPY ./src /code/

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --no-root --only main

CMD ["fastapi", "run", "--port", "80"]
# CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]ker 