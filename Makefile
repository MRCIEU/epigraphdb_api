.PHONY: clean data lint requirements docs

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROFILE = default
PROJECT_NAME = epigraphdb_api

ifndef API_PORT
API_PORT=8000
endif

#################################################################################
# Rules
#################################################################################

## ==== utils ====
__utils__:

## Unit tests (takes a LONG time!)
test:
	python -m pytest -vv

## Unit tests for api
test_api:
	python -m pytest -vv tests/api_tests

## Unit tests for paired graph
test_graph:
	python -m pytest -vv tests/graph_tests

## ==== codebase ====
__codebase__:

## Lint codebase with flake8
lint:
	python -m flake8 app tests scripts
	python -m mypy app tests scripts

## Format codebase with black
fmt:
	python -m autoflake --in-place --remove-all-unused-imports --recursive app tests scripts
	python -m isort -rc app tests scripts
	python -m black app tests scripts

## Generate documentation
docs:
	scripts/rmd.sh scripts/doc-templates/meta-nodes.Rmd
	scripts/rmd.sh scripts/doc-templates/meta-relationships.Rmd
	scripts/rmd.sh scripts/doc-templates/metrics.Rmd
	scripts/rmd.sh scripts/doc-templates/api-endpoints.Rmd

## ==== running the api ====
__run__:

## Start API server, default to 8000, overwrite with API_PORT make run
run:
	uvicorn app.main:app --reload \
	--port ${API_PORT}

## Start API server using port 80 (for docker)
run80:
	uvicorn app.main:app --reload \
	--host 0.0.0.0 --port 80


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "$$(tput bold)Params:$$(tput sgr0)"
	@echo "$$(tput setaf 6)API_PORT:$$(tput sgr0) ${API_PORT}"
	@echo
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}'
