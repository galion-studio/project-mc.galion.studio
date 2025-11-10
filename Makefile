# Titan Server - Makefile
# Quick commands for common operations
# ELON MODE: One command to do everything

.PHONY: help build start stop restart logs clean deploy test status

# Default target
.DEFAULT_GOAL := help

# Colors
BLUE := \033[0;34m
GREEN := \033[0;32m
NC := \033[0m

## help: Show this help message
help:
	@echo "$(BLUE)========================================"
	@echo "  TITAN SERVER - Quick Commands"
	@echo "========================================$(NC)"
	@echo ""
	@echo "Available commands:"
	@grep -E '^## ' Makefile | sed 's/## /  make /' | column -t -s ':'
	@echo ""

## build: Build the project
build:
	@echo "$(BLUE)Building Titan...$(NC)"
	./gradlew clean build
	@echo "$(GREEN)✓ Build complete$(NC)"

## start: Start all services
start:
	@echo "$(BLUE)Starting Titan services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Services started$(NC)"
	@make status

## stop: Stop all services
stop:
	@echo "$(BLUE)Stopping Titan services...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Services stopped$(NC)"

## restart: Restart all services
restart: stop start

## logs: Tail logs from all services
logs:
	docker-compose logs -f

## logs-proxy: Tail proxy logs
logs-proxy:
	docker-compose logs -f titan-proxy

## logs-hub: Tail hub server logs
logs-hub:
	docker-compose logs -f titan-hub

## logs-survival: Tail survival server logs
logs-survival:
	docker-compose logs -f titan-survival

## clean: Clean build artifacts and stop services
clean:
	@echo "$(BLUE)Cleaning...$(NC)"
	./gradlew clean
	docker-compose down -v
	@echo "$(GREEN)✓ Cleaned$(NC)"

## deploy: Quick deploy (build + restart)
deploy:
	@echo "$(BLUE)Deploying Titan...$(NC)"
	./gradlew clean build -x test
	docker-compose down
	docker-compose up -d --build
	@echo "$(GREEN)✓ Deployed$(NC)"
	@make status

## test: Run tests
test:
	@echo "$(BLUE)Running tests...$(NC)"
	./gradlew test
	@echo "$(GREEN)✓ Tests complete$(NC)"

## status: Show service status
status:
	@echo "$(BLUE)Service Status:$(NC)"
	@docker-compose ps
	@echo ""
	@echo "$(BLUE)Health:$(NC)"
	@./automation/monitoring/health-check.sh 2>/dev/null || echo "Health check script not executable"

## backup: Create backup
backup:
	@echo "$(BLUE)Creating backup...$(NC)"
	./automation/backup/backup.sh
	@echo "$(GREEN)✓ Backup complete$(NC)"

## bootstrap: Initial setup
bootstrap:
	@echo "$(BLUE)Bootstrapping Titan...$(NC)"
	./automation/setup/bootstrap.sh

## shell-proxy: Open shell in proxy container
shell-proxy:
	docker-compose exec titan-proxy sh

## shell-hub: Open shell in hub container
shell-hub:
	docker-compose exec titan-hub bash

## shell-postgres: Open PostgreSQL shell
shell-postgres:
	docker-compose exec postgres psql -U titan

## shell-redis: Open Redis shell
shell-redis:
	docker-compose exec redis redis-cli

## grafana: Open Grafana in browser
grafana:
	@echo "Opening Grafana..."
	@echo "URL: http://localhost:3000"
	@echo "Username: admin"
	@echo "Password: admin"

## ship: Ship it! (Full build and deploy)
ship: build deploy
	@echo "$(GREEN)"
	@echo "========================================" @echo "  🚀 SHIPPED!"
	@echo "========================================$(NC)"
	@echo "Connect: localhost:25565"

