-include backend/.env

up:
	docker-compose -f docker-compose.yml -f docker-compose.${ENV}.yml up --build

down:
	docker-compose -f docker-compose.yml -f docker-compose.${ENV}.yml down
