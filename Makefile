export PYTHONPATH=.

format:
	pre-commit run -a

start_min:
	docker-compose -f api_ugc/infra/docker-compose.min.yml up -d
	docker-compose -f api_ugc/docker-compose.api_ugc.yaml up -d

stop_min:
	docker-compose -f api_ugc/docker-compose.api_ugc.yaml down -v
	docker-compose -f api_ugc/infra/docker-compose.min.yml down -v

start:
	docker-compose -f api_ugc/infra/docker-compose.infra.yml up -d
	docker-compose -f api_ugc/docker-compose.api_ugc.yaml up -d

stop:
	docker-compose -f api_ugc/docker-compose.api_ugc.yaml down -v
	docker-compose -f api_ugc/infra/docker-compose.infra.yml down -v


