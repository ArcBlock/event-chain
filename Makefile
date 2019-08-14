TOP_DIR=.
ENV=~/.envs
README=$(TOP_DIR)/README.md

VERSION=$(strip $(shell cat version))
PYTHON_TARGET=event_chain/protos
CONFIGS=forge forge_release forge_test forge_default

dep:
	@echo "Install dependencies required for this repo..."
	@pip install -r requirements.txt
	@cd forge_symposia && yarn install

init: deploy-protocols simulate
	@echo "Repo initialized and ready to go!"

create_env:
	@pip install virtualenv
	@pip install virtualenvwrapper
	( \
		source /usr/local/bin/virtualenvwrapper.sh; \
		mkvirtualenv forge-env -p python3; \
		pip install -r requirements.txt; \
	)

watch:
	@make build
	@echo "Watching templates and slides changes..."
	@fswatch -o src/ | xargs -n1 -I{} make build

lint:
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

package-pypi:
	@python setup.py sdist bdist_wheel
	@echo "file packaged successfully!"

upload-pypi:
	@twine upload -r pypi dist/*
	@echo "file uploaded successfully!"

pypi: package-pypi upload-pypi clean-pypi-build

simulate:
	@export PYTHONPATH=. && python forge_symposia/server/simulation/simulate.py

deploy-protocols:
	@export PYTHONPATH=. && python protocols/deploy.py

run-server:
	@export PYTHONPATH=. && python forge_symposia/server/app.py

run-client:
	@cd forge_symposia && yarn start:client


include .makefiles/*.mk

.PHONY: build init travis-init install dep pre-build post-build all test doc precommit travis clean watch run bump-version create-pr