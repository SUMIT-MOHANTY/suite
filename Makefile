.PHONY: dev build

dev:
	@echo "Starting dev servers..."
	@cd backend && npm run dev &
	@cd frontend && npm run dev

build:
	@echo "Building apps..."
	@cd backend && npm run build
	@cd frontend && npm run build
