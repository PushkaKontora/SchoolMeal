#!/bin/bash

SCRIPT_PATH="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

ENV_FILE="$SCRIPT_PATH/../.env"
: > "$ENV_FILE"

docker build -t secret_generator "$SCRIPT_PATH/secret_generator"

add_secret() {
  alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#%^&*(-_=+)"
  secret=""

  for _ in {1..64}; do
    secret="$secret${alphabet:RANDOM%${#alphabet}:1}"
  done

  echo "$1=$secret" >> "$ENV_FILE"
}

echo "--------------------------------------------------"
echo "Для выбора дефолтного значения нажмите Enter"
echo "--------------------------------------------------"

read -r -p "Какие композы использовать[docker-compose.yaml:docker-compose.stand.yaml:docker-compose.dev.yaml]: "
echo "COMPOSE_FILE=${REPLY:-docker-compose.yaml:docker-compose.stand.yaml:docker-compose.dev.yaml}" >> "$ENV_FILE"

read -r -p "Введите тайм-зону[Asia/Ekaterinburg]: "
echo "TZ=${REPLY:-Asia/Ekaterinburg}" >> "$ENV_FILE"

echo "" >> "$ENV_FILE"
echo "#---------DATABASE------------" >> "$ENV_FILE"

read -r -p "Введите адрес СУБД[postgres-server]: "
echo "POSTGRES_HOST=${REPLY:-postgres-server}" >> "$ENV_FILE"

read -r -p "Введите порт СУБД[5432]: "
echo "POSTGRES_PORT=${REPLY:-5432}" >> "$ENV_FILE"

read -r -p "Введите имя базы данных[school_meal]: "
echo "POSTGRES_DB=${REPLY:-school_meal}" >> "$ENV_FILE"

read -r -p "Введите имя пользователя СУБД[postgres]: "
echo "POSTGRES_USER=${REPLY:-postgres}" >> "$ENV_FILE"

read -r -p "Введите пароль пользователя СУБД[postgres]: "
echo "POSTGRES_PASSWORD=${REPLY:-postgres}" >> "$ENV_FILE"

echo "" >> "$ENV_FILE"
echo "#-----------JWT------------" >> "$ENV_FILE"

add_secret "JWT_SECRET"

read -r -p "Введите время жизни JWT доступа[P0DT0H30M0S]: "
echo "JWT_ACCESS_LIFETIME=${REPLY:-P0DT0H30M0S}" >> "$ENV_FILE"

read -r -p "Введите время жизни JWT обновления[P30DT0H0M0S]: "
echo "JWT_REFRESH_LIFETIME=${REPLY:-P30DT0H0M0S}" >> "$ENV_FILE"
