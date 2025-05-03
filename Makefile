.PHONY: setup up prod down alldelete django mysql nginx

include .env

setup:
	@make up
	@make ps
down:
	docker compose down
up:
	docker compose up
prod:
	docker compose -f docker-compose.prod.yaml up
alldelete:
	docker compose down --rmi all --volumes --remove-orphans
django:
	docker exec -it --user 1000:1000 ${COMPOSE_PROJECT_NAME}-app-1 bash
mysql:
	docker exec -it --user 1000:1000 ${COMPOSE_PROJECT_NAME}-db-1 bash
nginx:
	docker exec -it --user 1000:1000 ${COMPOSE_PROJECT_NAME}-web-1 bash
tailwind:
	docker compose run --rm app npm install



