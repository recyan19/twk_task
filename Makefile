help: ## show this help
	@echo 'usage: make [target] ...'
	@echo ''
	@echo 'targets:'
	@egrep '^(.+)\:\ .*##\ (.+)' ${MAKEFILE_LIST} | sed 's/:.*##/#/' | column -t -c 2 -s '#'

venv:  ## create python venv
	python3 -m venv venv

install:  ## install requirements
	venv/bin/pip install -r requirements.txt

test: ## run tests with pytest
	docker-compose up -d mongo
	venv/bin/pytest --cov=cars_app tests

run: ## run in local
	docker-compose up -d mongo
	PORT=8080 venv/bin/watchmedo auto-restart -d app -p '*.py' -- venv/bin/python -m cars_app.main

run_in_docker: ## run in docker
	docker-compose build
	docker-compose up -d
