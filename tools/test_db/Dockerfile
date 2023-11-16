FROM python:3.10.10-slim-bullseye

ARG POETRY_HOME=/opt/poetry
ARG POETRY_VERSION=1.6.1
ARG USER=test_db
ARG APP_DIR=/test_db

ENV PATH=$POETRY_HOME/bin:$PATH
ENV PYTHONPATH=$APP_DIR/src:$PYTHONPATH

WORKDIR $APP_DIR

RUN useradd -m $USER

RUN apt update && \
    pip install poetry==$POETRY_VERSION

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY src $APP_DIR/src

EXPOSE 8000
USER $USER

ENTRYPOINT python src/main.py