export PYTHONPATH=.

format:
	pre-commit run -a

start_api_min:
	docker-compose -f api_ugc/infra/docker-compose.min.yml up -d
	docker-compose -f api_ugc/docker-compose.api_ugc.yaml up -d

stop_api_min:
	docker-compose -f api_ugc/docker-compose.api_ugc.yaml down -v
	docker-compose -f api_ugc/infra/docker-compose.min.yml down -v
	


