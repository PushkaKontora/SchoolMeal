-include backend/.env

up:
	docker-compose -f docker-compose.yml -f docker-compose.${ENV}.yml up -d

down:
	docker-compose -f docker-compose.yml -f docker-compose.${ENV}.yml down

build:
	docker-compose -f docker-compose.yml -f docker-compose.${ENV}.yml build
