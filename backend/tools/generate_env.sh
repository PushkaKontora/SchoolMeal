#!/bin/bash

SCRIPT_PATH="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

read -r -p "Введите имя файла [.env]: "
ENV_FILE="$SCRIPT_PATH/../${REPLY:-.env}"

docker build -t env_generator "$SCRIPT_PATH/env_generator" && \
docker run -it env_generator /bin/sh -c "python main.py && cat env" > "$ENV_FILE"
