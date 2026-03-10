.PHONY: build dev up down lint
build:
	docker-compose build
dev:
	docker-compose up --build
up:
	docker-compose up -d
down:
	docker-compose down
lint:
	npm run lint
