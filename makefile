run:
	docker compose -f docker-compose.yml up --build
dev:
	docker compose -f docker-compose.dev.yml up --build
