.PHONY: clean data lint requirements docs

#################################################################################
# Rules
#################################################################################

## ==== codebase ====
__codebase__:

## check for issues in env configs
check:
	python -m scripts.check

## Format codebase
fmt:
	python -m autoflake \
		--in-place --remove-all-unused-imports --recursive \
		app tests scripts epigraphdb_common_utils
	python -m isort -rc app tests scripts epigraphdb_common_utils
	python -m black app tests scripts epigraphdb_common_utils

## Lint codebase
lint:
	python -m flake8 app tests scripts epigraphdb_common_utils
	python -m mypy app tests scripts epigraphdb_common_utils

## ==== utils ====
__utils__:

## Unit tests (takes a LONG time!)
test:
	python -m pytest -vv

## Generate documentation
docs:
	scripts/rmd.sh scripts/doc-templates/meta-nodes.Rmd
	scripts/rmd.sh scripts/doc-templates/meta-relationships.Rmd
	scripts/rmd.sh scripts/doc-templates/metrics.Rmd
	scripts/rmd.sh scripts/doc-templates/api-endpoints.Rmd

## ==== running the api ====
__run__:

## Start API server, port: 80
run:
	python -m scripts.check
	uvicorn app.main:app --reload \
	--host 0.0.0.0 --port 80


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

.PHONY: help
help:
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
