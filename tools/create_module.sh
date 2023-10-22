#!/bin/bash

create_module() {
  filename="$1.py"

  if [[ -e "$filename" ]]; then
    return
  fi

  : > "$filename"
  echo "Создан модуль $(realpath "$filename")"
}

create_package() {
  mkdir -p "$1"
  create_module "$1/__init__"
}

read -r -p "Введите имя модуля: " module_name

create_package "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/../app/$module_name" && cd "$_"

create_package "domain"
for module in model errors; do
  create_module "domain/$module"
done

create_package "application"
for module in adapters repositories services; do
  create_module "application/$module"
done

create_package "infrastructure"
create_module "infrastructure/adapters"
create_package "infrastructure/db"
for module in models repositories; do
  create_module "infrastructure/db/$module"
done

create_package "gateway"
create_package "gateway/internal"
create_package "gateway/rest" && create_module "gateway/rest/dependencies"