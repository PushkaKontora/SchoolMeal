FROM python:3.10-alpine3.17

WORKDIR /app

COPY Pipfile ./

ARG PIPENV_OPTIONS=""
RUN apk add make && \
    pip install pipenv && \
    pipenv install --system --skip-lock $PIPENV_OPTIONS

COPY . .

CMD make migrate && gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000