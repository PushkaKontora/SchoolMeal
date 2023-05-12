dev:
	uvicorn app.main:app --reload

run:
	gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

lint:
	isort . & \
	flake8 --config=setup.cfg & \
	black . --config=pyproject.toml

pshell:
	PIPENV_DONT_LOAD_ENV=1 pipenv shell

migration:
	alembic revision --autogenerate -m "${n}"

migrate:
	alembic upgrade head

test:
	pytest tests -v

unit:
	pytest tests -v -m unit

integration:
	pytest tests -v -m integration
