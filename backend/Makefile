venv:
	PIPENV_DONT_LOAD_ENV=1 pipenv shell

format:
	isort . & \
	flake8 --config setup.cfg & \
	black . --config pyproject.toml

lint:
	isort --check --diff .
	flake8 --config setup.cfg
	black --check --config pyproject.toml .
	mypy --cache-dir=/dev/null --config-file=setup.cfg app

migration:
	read -p "Введите имя миграции: " MIGRATION_NAME; \
	alembic revision --autogenerate -m "$$MIGRATION_NAME"

migrate:
	@echo "Для применения миграций должна быть запущена БД локально ( docker-compose up -d postgres-server )"; \
	alembic upgrade head

test:
	@echo "Для выполнения тестов должна быть запущена БД локально ( docker-compose up -d postgres-server )"; \
	pytest tests -v
