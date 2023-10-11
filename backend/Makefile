SOURCE = app
TESTS = tests
ALL = $(SOURCE) $(TESTS)

VENV = .venv
BIN_DIR = $(VENV)/bin

venv:
	python3.10 -m venv $(VENV)
	$(BIN_DIR)/python -m pip install --upgrade pip
	$(BIN_DIR)/python -m pip install poetry~=1.6.0
	$(BIN_DIR)/python -m poetry install

format:
	$(BIN_DIR)/isort $(ALL)
	$(BIN_DIR)/flake8 --config setup.cfg $(ALL)
	$(BIN_DIR)/black . --config pyproject.toml $(ALL)

lint:
	$(BIN_DIR)/isort --check --diff $(ALL)
	$(BIN_DIR)/flake8 --config setup.cfg $(ALL)
	$(BIN_DIR)/black --check --config pyproject.toml $(ALL)
	$(BIN_DIR)/mypy --cache-dir=/dev/null --config-file=setup.cfg $(SOURCE)
	mypy

mypy:
	$(BIN_DIR)/mypy --cache-dir=/dev/null --config-file=setup.cfg $(SOURCE)

migration:
	read -p "Введите имя миграции: " MIGRATION_NAME; \
	$(BIN_DIR)/alembic revision --autogenerate -m "$$MIGRATION_NAME"

migrate:
	@echo "Для применения миграций должна быть запущена БД локально ( docker-compose up -d postgres-server )"; \
	$(BIN_DIR)/alembic upgrade head

test:
	$(BIN_DIR)/pytest tests -v
