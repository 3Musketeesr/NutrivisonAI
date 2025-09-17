
# Colors
GREEN=\033[32m
BLUE=\033[34m
RED=\033[31m
YELLOW=\033[33m
RESET=\033[0m

.PHONY: venv deps up up-watch down clean

venv:
	@echo "$(BLUE)[setup]$(RESET) creating venv"
	python3 -m venv .venv

deps:
	@echo "$(BLUE)[deps]$(RESET) installing"
	.venv/bin/pip install -r ./requirements.txt

up:
	@echo "$(GREEN)[up]$(RESET) docker compose up"
	docker compose up

up-watch:
	@echo "$(GREEN)[up]$(RESET) watch"
	docker compose up --watch

up-watch-build:
	@echo "$(GREEN)[up]$(RESET) watch and build"
	docker compose up --watch --build

down:
	@echo "$(YELLOW)[down]$(RESET) stopping"
	docker compose down --remove-orphans

clean:
	@echo "$(RED)[clean]$(RESET) pruning"
	docker system prune -f