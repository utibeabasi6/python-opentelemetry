up: bootstrap
	@docker-compose up 

bootstrap:
	@python3 scripts/bootstrap.py

build: bootstrap
	@docker-compose up --build

down:
	@docker-compose down