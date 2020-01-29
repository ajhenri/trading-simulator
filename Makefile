.PHONY: help

help:
	@awk '/^#/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) | column -s: -t

## Build the Docker images
build:
	docker-compose build

## Creates containers and starts services
up:
	docker-compose up -d

## Stops services and removes containers
down:
	docker-compose down

## Shell into the web container
sh-web:
	docker-compose exec -u root web bash

## Shell into the DB container
sh-db:
	docker-compose exec postgres psql -w --username "postgres" --dbname "trading_simulator"

## Migrate with alembic, e.g. m="initial table structure"
migration:
	docker-compose exec web alembic revision --autogenerate -m "$(m)"

## Run all migrations
migrate-up:
	docker-compose exec web alembic upgrade head

## Rollback last migration
migrate-down:
	docker-compose exec web alembic downgrade -1