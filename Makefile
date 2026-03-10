.PHONY: up down seed

# Bring up the staging environment with all services
up:
	docker compose -f docker-compose.staging.yml --env-file .env.staging up --build -d

# Bring down the staging environment
down:
	docker compose -f docker-compose.staging.yml --env-file .env.staging down

# Seed the database with initial data (run after services are up)
seed:
	@echo "Placeholder: run database migrations and seed data"
	@echo "docker compose -f docker-compose.staging.yml --env-file .env.staging exec api npm run migrate && npm run seed"
	@echo "In real implementation, uncomment and run:"
	# docker compose -f docker-compose.staging.yml --env-file .env.staging exec api npm run migrate
	# docker compose -f docker-compose.staging.yml --env-file .env.staging exec api npm run seed
