# Makefile

# Variables
PYTHON = poetry run
DOCKER = docker-compose

# Targets
all: format lint test

format:
	$(PYTHON) black .
	$(PYTHON) isort .

lint:
	$(PYTHON) flake8 .

test:
	$(PYTHON) pytest

down:
	$(DOCKER) down

build:
	$(DOCKER) build

up:
	$(DOCKER) up

up-d:
	$(DOCKER) up -d

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache