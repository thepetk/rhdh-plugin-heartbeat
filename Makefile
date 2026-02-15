.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: test
test:
	uv run pytest

.PHONY: ruff
ruff:
	uv run ruff check --fix src/ tests/
	uv run ruff format src/ tests/

.PHONY: ty
ty:
	uvx ty check

.PHONY: pre-commit-install
pre-commit-install: ## Install pre-commit hooks
	uv run pre-commit install