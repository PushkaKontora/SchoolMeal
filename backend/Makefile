SOURCE = app
TESTS = tests
ALL = $(SOURCE) $(TESTS)

VENV = .venv
BIN_DIR = $(VENV)/bin

ENV_VARIABLES=JWT_SECRET=aaaaaaaaaaaaaaaaaaaaaa

venv:
	python3.10 -m venv $(VENV)
	$(BIN_DIR)/python -m pip install --upgrade pip
	$(BIN_DIR)/python -m pip install poetry~=1.6.0
	$(BIN_DIR)/python -m poetry install

format:
	@echo "Formatting isort" && $(BIN_DIR)/isort $(ALL)
	@echo "Formatting black" && $(BIN_DIR)/black . --config pyproject.toml $(ALL)
	@echo "Formatting autoflake" && $(BIN_DIR)/autoflake --recursive --in-place --remove-all-unused-imports --ignore-init-module-imports $(ALL)
	@echo "Formatting unify" && $(BIN_DIR)/unify --in-place --recursive --quote '"' $(ALL)

lint:
	@echo "Linting isort" && $(BIN_DIR)/isort --jobs 4 --check --diff $(ALL)
	@echo "Linting flake8" && $(BIN_DIR)/flake8 --jobs 4 --statistics --show-source --config setup.cfg $(ALL)
	@echo "Linting black" && $(BIN_DIR)/black --workers 4 --check --config pyproject.toml $(ALL)
	@echo "Linting mypy" && $(BIN_DIR)/mypy --cache-dir=/dev/null --config-file=setup.cfg $(SOURCE)

mypy:
	$(BIN_DIR)/mypy --cache-dir=/dev/null --config-file=setup.cfg $(SOURCE)

migration:
	@echo "Для выполнения автогенерации должна быть запущена БД локально с дефолтными значениями ( docker-compose up -d postgres-server )"; \
	read -p "Введите имя миграции: " MIGRATION_NAME; \
	$(ENV_VARIABLES) $(BIN_DIR)/alembic downgrade base && $(ENV_VARIABLES) $(BIN_DIR)/alembic upgrade head && $(ENV_VARIABLES) $(BIN_DIR)/alembic revision --autogenerate -m "$$MIGRATION_NAME"

migrate:
	$(ENV_VARIABLES) $(BIN_DIR)/alembic upgrade head

downgrade:
	$(ENV_VARIABLES) $(BIN_DIR)/alembic downgrade -1

test:
	$(ENV_VARIABLES) $(BIN_DIR)/pytest -vv -s tests

ci: lint test