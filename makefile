SRC = walletsaver
COV = --cov=$(SRC) --cov-branch --cov-report=term-missing

DB_NAME = wsaver
DB_USER = wsaveruser
DB_CREATE = CREATE DATABASE $(DB_NAME);
DB_POST_CREATE = \
CREATE USER $(DB_USER) WITH PASSWORD 'wsaver4pwd'; \
ALTER ROLE $(DB_USER) SET client_encoding TO 'utf8'; \
ALTER ROLE $(DB_USER) SET default_transaction_isolation TO 'read committed'; \
ALTER ROLE $(DB_USER) SET timezone TO 'UTC'; \
GRANT ALL PRIVILEGES ON DATABASE $(DB_NAME) TO $(DB_USER);


all:
	@grep -E "^\w+:" makefile | cut -d: -f1

up:
	docker-compose up -d

dbsetup:
	-docker exec -u postgres wsaver-db psql -c "$(DB_CREATE)"
	-docker exec -u postgres wsaver-db psql -c "$(DB_POST_CREATE)"

install:
	pip install -r requirements.txt

clean:
	find . -type f -name *.pyc -delete

test:
	pytest $(COV)

cov-report:
	coverage report -m
