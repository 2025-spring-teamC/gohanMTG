.PHONY: setup up prod down alldelete django mysql

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
	docker exec -it --user 1000:1000 django bash
mysql:
	docker exec -it --user 1000:1000 mysql bash
nginx:
	docker exec -it --user 1000:1000 nginx bash
tailwind:
	docker compose run --rm app npm install



