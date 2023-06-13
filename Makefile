-include backend/.env

up:
	docker-compose -f docker-compose.yml -f docker-compose.${ENV}.yml up -d

# $p [params string]
down:
	docker-compose -f docker-compose.yml -f docker-compose.${ENV}.yml down $(if $p,$p,)

build:
	docker-compose -f docker-compose.yml -f docker-compose.${ENV}.yml build

push:
	docker-compose -f docker-compose.yml -f docker-compose.${ENV}.yml push

pull:
	docker-compose -f docker-compose.yml -f docker-compose.${ENV}.yml pull

# $c [container name]
shell:
	docker-compose -f docker-compose.yml -f docker-compose.${ENV}.yml run ${c} /bin/sh