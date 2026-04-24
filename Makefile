install:
	$(MAKE) -C backend install
	$(MAKE) -C frontend install

install-dev:
	$(MAKE) -C backend install-dev
	$(MAKE) -C frontend install-dev

format:
	$(MAKE) -C backend format

lint:
	$(MAKE) -C backend lint

test:
	$(MAKE) -C backend test
	$(MAKE) -C frontend test

lock:
	$(MAKE) -C backend lock
	$(MAKE) -C frontend lock

lock-upgrade:
	$(MAKE) -C backend lock-upgrade

frontend-build:
	$(MAKE) -C frontend build

docker-build:
	docker compose build

docker-run:
	docker compose up

.PHONY: install install-dev format lint test lock lock-upgrade \
        frontend-build \
        docker-build docker-run
