FROM python:3.10.10-slim-bullseye

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VERSION=1.6.1
ENV PATH=$POETRY_HOME/bin:$PATH

WORKDIR /school_meal

RUN apt update && \
    apt install make && \
    pip install -U pip && \
    pip install pip install poetry==$POETRY_VERSION

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . .

ENTRYPOINT ["sh", "docker-entrypoint.sh"]