TOP_DIR=.
ENV=~/.envs
README=$(TOP_DIR)/README.md

VERSION=$(strip $(shell cat version))
PYTHON_TARGET=event_chain/protos
CONFIGS=forge forge_release forge_test forge_default

build:
	@echo "Building the software..."

init: install dep create_env
	@echo "Initializing the repo..."
	@git submodule update --init --recursive

create_env:
	@pip install virtualenv
	@pip install virtualenvwrapper
	( \
		source /usr/local/bin/virtualenvwrapper.sh; \
		mkvirtualenv forge-python-sdk; \
		pip install -r requirements.txt; \
		pre-commit install; \
	)

add_precommit_hook:
	@pre-commit install

travis-init: add_precommit_hook
	@echo "Initialize software required for travis (normally ubuntu software)"

install:
	@echo "Install software required for this repo..."

dep:
	@echo "Install dependencies required for this repo..."

pre-build: install dep
	@echo "Running scripts before the build..."

post-build:
	@echo "Running scripts after the build is done..."

all: pre-build build post-build

test:
	@echo "Running test suites..."

lint:
	@echo "Linting the software..."
	@python .git/hooks/pre-commit

doc:
	@echo "Building the documenation..."

precommit: dep lint doc build test

travis: precommit

travis-deploy: release
	@echo "Deploy the software by travis"

clean:
	@echo "Cleaning the build..."

watch:
	@make build
	@echo "Watching templates and slides changes..."
	@fswatch -o src/ | xargs -n1 -I{} make build

run:
	@echo "Running the software..."

check-style:
	@flake8 event_chain/application test

build-all-protos:
	@rm -r $(PYTHON_TARGET)/protos
	@mkdir -p $(PYTHON_TARGET)/protos;mkdir -p $(PYTHON_TARGET)/raw_protos
	@echo "Buiding all protobuf files..."
	@python -m grpc_tools.protoc -I ./$(PYTHON_TARGET)/raw_protos --python_out=./$(PYTHON_TARGET)/protos --grpc_python_out=./$(PYTHON_TARGET)/protos ./$(PYTHON_TARGET)/raw_protos/*.proto
	@sed -i -E 's/^import.*_pb2/from . \0/' ./$(PYTHON_TARGET)/protos/*.py
	@echo "All protobuf files are built and ready to use!.."
	@for filename in ./$(PYTHON_TARGET)/protos/*.py; do \
	 echo "from event_chain.protos.protos.$$(basename $$filename .py) import *" >>$(PYTHON_TARGET)/protos/__init__.py; \
	 done

clean-pypi-build:
	@rm -rf build
	@rm -rf dist
	@echo "All build and dist folders are cleaned!"

package-pypi: clean-pypi-build
	@python setup.py sdist bdist_wheel
	@echo "file packaged successfully!"

upload-pypi:
	@twine upload -r pypi dist/*
	@echo "file uploaded successfully!"

pypi: package-pypi upload-pypi clean-pypi-build

include .makefiles/*.mk

.PHONY: build init travis-init install dep pre-build post-build all test doc precommit travis clean watch run bump-version create-pr