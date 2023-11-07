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

echo "BRANCH_TAG=master" >> "$ENV_FILE"

read -r -p "Какие композы использовать[docker-compose.yaml:docker-compose.stand.yaml:docker-compose.dev.yaml]: "
echo "COMPOSE_FILE=${REPLY:-docker-compose.yaml:docker-compose.stand.yaml:docker-compose.dev.yaml}" >> "$ENV_FILE"

echo "" >> "$ENV_FILE"
echo "#---------Сервис------------" >> "$ENV_FILE"

read -p "Указать отображение Swagger UI? (Y/n)" -n 1 -s -r yn; echo
  if [[ "$yn" =~ ^([yY])$ ]] || [[ $yn = "" ]]
  then
    read -e -p "Значение по умолчанию [false]: "
    if [[ $REPLY = "" ]]
    then
      echo "SHOW_SWAGGER_UI=false" >> $ENV_FILE ; echo
    else
      echo "SHOW_SWAGGER_UI=$REPLY" >> $ENV_FILE ; echo
    fi
  else
    # оставить все по умолчанию и закомментированным
    echo "SHOW_SWAGGER_UI=false" >> $ENV_FILE ; echo
  fi

echo "" >> "$ENV_FILE"
echo "#---------СУБД------------" >> "$ENV_FILE"

read -r -p "Введите адрес СУБД[postgres-server]: "
echo "DB_HOST=${REPLY:-postgres-server}" >> "$ENV_FILE"

read -r -p "Введите порт СУБД[5432]: "
echo "DB_PORT=${REPLY:-5432}" >> "$ENV_FILE"

read -r -p "Введите имя базы данных[school_meal]: "
echo "DB_NAME=${REPLY:-school_meal}" >> "$ENV_FILE"

read -r -p "Введите имя пользователя СУБД[postgres]: "
echo "DB_USER=${REPLY:-postgres}" >> "$ENV_FILE"

read -r -p "Введите пароль пользователя СУБД[postgres]: "
echo "DB_PASSWORD=${REPLY:-postgres}" >> "$ENV_FILE"

echo "" >> "$ENV_FILE"
echo "#-----------JWT------------" >> "$ENV_FILE"

add_secret "JWT_SECRET"
