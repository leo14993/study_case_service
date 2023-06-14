# Variables
GIT_CURRENT_BRANCH := ${shell git symbolic-ref --short HEAD}
SRC_DIR := ./

redis_create:
	@docker run --name redis-offer-query -d -p 6382:6379 redis:alpine 
	@echo 'Created redis'
	@echo 'Set env HOST with this value => localhost'
	@echo 'Set env PORT with this value => 6382'

setup_dev: redis_create
	@echo "---- Upgrading PIP ----"
	@pip install --upgrade pip
	@echo ""
	@echo ""
	@echo "---- Installing DEV Python dependencies ----"
	@pip install -r requirements-dev.txt
	@echo ""
	@echo ""
	@echo "---- Creating .env based on .env.example ----"
	@cp .env.example .env

clean:
	@echo "---- Cleaning up .pyc files ----"
	@find . -name '*.pyc' -delete
	@rm -rf `find . -type d -name "__pycache__"`
	@rm -rf `find . -type d -name ".pytest_cache"`
	@rm -rf `find . -type d -name "htmlcov"`
	@echo "---- Cleaned ----"

redis_start:
	@docker start redis-offer-query
	@echo 'Started cache'


redis_stop:
	@docker stop redis-offer-query
	@echo 'Stoped cache'

isort:
	@isort  . 

run: redis_start
ifeq ($(gc),)
	@uvicorn src.main:app --port 8001 --reload 
else
	@gunicorn -c gunicorn.py src.main:app
endif

coverage:
	@echo "---- Running tests coverage ----"
	@PYTHONPATH=$(BASE_DIR) pytest --cov=$(SRC_DIR)
	@coverage-badge > coverage.svg

