install:
	$(MAKE) -C backend install

install-dev:
	$(MAKE) -C backend install-dev

format:
	$(MAKE) -C backend format

lint:
	$(MAKE) -C backend lint

test:
	$(MAKE) -C backend test

lock:
	$(MAKE) -C backend lock

lock-upgrade:
	$(MAKE) -C backend lock-upgrade

frontend-install:
	$(MAKE) -C frontend install

frontend-test:
	$(MAKE) -C frontend test

frontend-build:
	$(MAKE) -C frontend build

docker-build:
	docker compose build

docker-run:
	docker compose up

.PHONY: install install-dev format lint test lock lock-upgrade \
        frontend-install frontend-test frontend-build \
        docker-build docker-run
