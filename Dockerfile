FROM python:3.11-buster

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

ENV PYTHONPATH "${PYTHONPATH}:/app/app"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

COPY app ./app

RUN touch README.md

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "-m", "app.main"]

EXPOSE 5000

