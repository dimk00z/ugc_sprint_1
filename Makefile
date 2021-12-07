export PYTHONPATH=.

format:
	pre-commit run -a

# TODO update make file

# export PYTHONPATH=auth/src
# export DOCKER_COMPOSE_FILES=-f docker-compose.yml -f docker-compose.api.yml


# build:
# 	docker-compose $(DOCKER_COMPOSE_FILES) build

# start:
# 	docker-compose $(DOCKER_COMPOSE_FILES) up -d

# stop:
# 	docker-compose $(DOCKER_COMPOSE_FILES) down

# restart:
# 	docker-compose $(DOCKER_COMPOSE_FILES) down
# 	docker-compose $(DOCKER_COMPOSE_FILES) up -d

# test:
# 	pytest --disable-pytest-warnings -v -s tests/

# coverage:
# 	pytest --disable-pytest-warnings --cov-report html --cov=auth -v -s tests/
