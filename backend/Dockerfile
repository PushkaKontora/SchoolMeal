FROM python:3.10.10-slim-bullseye as base

ARG POETRY_HOME=/opt/poetry
ARG POETRY_VERSION=1.6.1
ARG USER=school_meal
ARG APP_DIR=/school_meal

ENV PATH=$POETRY_HOME/bin:$PATH

WORKDIR $APP_DIR

RUN useradd -m $USER

RUN apt update && \
    apt install make && \
    pip install -U pip && \
    pip install poetry==$POETRY_VERSION

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY docker-entrypoint.sh $APP_DIR
COPY alembic.ini $APP_DIR
COPY alembic $APP_DIR/alembic
COPY app $APP_DIR/app


FROM base as test

COPY Makefile $APP_DIR
COPY setup.cfg $APP_DIR
COPY tests $APP_DIR/tests

RUN poetry isntall --no-interaction --no-ansi

RUN make BIN_DIR=/usr/local/bin ci


FROM base as final

EXPOSE 8000
USER $USER

ENTRYPOINT ["sh", "./docker-entrypoint.sh"]