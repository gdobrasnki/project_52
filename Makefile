PYTHON_FILES = $(shell find . -name \*.py)

local: deps lint unit-test build-local smoke-test-local
all: local
default: local

deps:
	@echo "=== dependencies ==="
	@pip install --upgrade pip
	@pip install -r requirements.txt

lint:
	@echo "=== linting ==="
	@pylint -E $(PYTHON_FILES)

unit-test:
	@echo "=== unit testing ==="
	# TODO @pytest

build-local:
	@echo "=== build local ==="
	# TODO @docker-compose up -d

smoke-test-local:
	@echo "=== smoke testing local ==="
	# TODO curl http://localhost:5000

