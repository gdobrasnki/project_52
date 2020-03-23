PYTHON_FILES = $(shell find . -name \*.py)
PROJECT_DIR='helpnextdoor'

default: local
deps: pip
test: lint unit-test build-local smoke-test-local
local: deps test 

pip:
	@echo "=== Installing Python dependencies ==="
	@pip install -r requirements.txt

lint:
	@echo "=== Python Linting ==="
	@pylint -E $(PYTHON_FILES)

unit-test:
	@echo "=== Python Unit Testing ==="
	# TODO @pytest

build-local:
	@echo "=== Build Local ==="
	@docker-compose up -d

smoke-test-local:
	@echo "=== smoke testing local ==="
	@docker ps
	@sleep 10
	@docker ps
	curl -I 0.0.0.0:5000
