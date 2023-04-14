dev:
	uvicorn app.main:app --reload

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
	pytest tests

unit:
	pytest tests -m unit

integration:
	pytest tests -m integration
