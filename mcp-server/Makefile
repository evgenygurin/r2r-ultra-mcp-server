.PHONY: help install install-dev test test-verbose test-coverage lint format clean run run-http inspect deploy-check commit-check all

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ Help

help: ## Display this help message
	@echo "$(BLUE)R2R Ultra MCP Server v3.0 - Makefile Commands$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make $(GREEN)<target>$(NC)\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Installation

install: ## Install production dependencies
	@echo "$(BLUE)📦 Installing production dependencies...$(NC)"
	uv sync --no-dev
	@echo "$(GREEN)✅ Production dependencies installed$(NC)"

install-dev: ## Install all dependencies (including dev tools)
	@echo "$(BLUE)📦 Installing all dependencies...$(NC)"
	uv sync
	@echo "$(GREEN)✅ All dependencies installed$(NC)"

##@ Testing

test: ## Run all tests
	@echo "$(BLUE)🧪 Running tests...$(NC)"
	pytest tests/
	@echo "$(GREEN)✅ Tests passed$(NC)"

test-verbose: ## Run tests with verbose output
	@echo "$(BLUE)🧪 Running tests (verbose)...$(NC)"
	pytest tests/ -v

test-coverage: ## Run tests with coverage report
	@echo "$(BLUE)🧪 Running tests with coverage...$(NC)"
	pytest tests/ --cov=server --cov-report=html --cov-report=term
	@echo "$(GREEN)✅ Coverage report generated in htmlcov/$(NC)"

test-watch: ## Run tests in watch mode (requires pytest-watch)
	@echo "$(BLUE)🧪 Running tests in watch mode...$(NC)"
	ptw tests/

##@ Code Quality

lint: ## Run linter (ruff)
	@echo "$(BLUE)🔍 Running linter...$(NC)"
	ruff check .
	@echo "$(GREEN)✅ Linting complete$(NC)"

lint-fix: ## Run linter with auto-fix
	@echo "$(BLUE)🔧 Running linter with auto-fix...$(NC)"
	ruff check --fix .
	@echo "$(GREEN)✅ Auto-fixes applied$(NC)"

format: ## Format code with ruff
	@echo "$(BLUE)✨ Formatting code...$(NC)"
	ruff format .
	@echo "$(GREEN)✅ Code formatted$(NC)"

format-check: ## Check code formatting without changes
	@echo "$(BLUE)🔍 Checking code format...$(NC)"
	ruff format --check .

##@ Development

run: ## Run server (stdio transport)
	@echo "$(BLUE)🚀 Starting R2R Ultra MCP Server (stdio)...$(NC)"
	python server.py

run-http: ## Run server (HTTP/SSE transport on port 8000)
	@echo "$(BLUE)🚀 Starting R2R Ultra MCP Server (HTTP/SSE)...$(NC)"
	python server.py --transport sse --port 8000

run-dev: ## Run server with inspector
	@echo "$(BLUE)🔍 Starting server with MCP Inspector...$(NC)"
	fastmcp dev server.py:mcp

inspect: ## Inspect server capabilities
	@echo "$(BLUE)🔍 Inspecting server...$(NC)"
	fastmcp inspect server.py:mcp

inspect-json: ## Inspect server and output JSON
	@echo "$(BLUE)🔍 Inspecting server (JSON output)...$(NC)"
	fastmcp inspect server.py:mcp --format mcp

##@ Deployment

deploy-check: ## Verify server is ready for deployment
	@echo "$(BLUE)🔍 Running deployment checks...$(NC)"
	@echo "1. Checking Python syntax..."
	@python -m py_compile server.py && echo "$(GREEN)✅ Syntax OK$(NC)" || (echo "$(RED)❌ Syntax error$(NC)" && exit 1)
	@echo "2. Inspecting server..."
	@fastmcp inspect server.py:mcp > /dev/null && echo "$(GREEN)✅ Server loads$(NC)" || (echo "$(RED)❌ Server failed to load$(NC)" && exit 1)
	@echo "3. Running tests..."
	@pytest tests/ -q && echo "$(GREEN)✅ Tests pass$(NC)" || (echo "$(RED)❌ Tests failed$(NC)" && exit 1)
	@echo "4. Checking linter..."
	@ruff check . && echo "$(GREEN)✅ Linting OK$(NC)" || (echo "$(RED)❌ Linting errors$(NC)" && exit 1)
	@echo ""
	@echo "$(GREEN)✅ All deployment checks passed!$(NC)"
	@echo "$(BLUE)Ready to deploy to FastMCP Cloud$(NC)"

commit-check: lint format-check test ## Run all checks before commit
	@echo "$(GREEN)✅ All pre-commit checks passed!$(NC)"

##@ Cleanup

clean: ## Clean temporary files and caches
	@echo "$(BLUE)🧹 Cleaning temporary files...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage 2>/dev/null || true
	@echo "$(GREEN)✅ Cleanup complete$(NC)"

clean-all: clean ## Clean everything including virtual environment
	@echo "$(BLUE)🧹 Deep cleaning...$(NC)"
	rm -rf .venv/
	@echo "$(GREEN)✅ Deep cleanup complete$(NC)"

##@ Git & GitHub

git-status: ## Show git status
	@git status

git-diff: ## Show git diff
	@git diff

commit: ## Quick commit (usage: make commit MSG="your message")
	@if [ -z "$(MSG)" ]; then \
		echo "$(RED)❌ Error: MSG is required$(NC)"; \
		echo "Usage: make commit MSG=\"your commit message\""; \
		exit 1; \
	fi
	@echo "$(BLUE)📝 Creating commit...$(NC)"
	git add .
	git commit -m "$(MSG)"
	@echo "$(GREEN)✅ Commit created$(NC)"

push: ## Push to current branch
	@echo "$(BLUE)⬆️ Pushing to remote...$(NC)"
	git push
	@echo "$(GREEN)✅ Pushed successfully$(NC)"

push-main: ## Push to main branch
	@echo "$(BLUE)⬆️ Pushing to main...$(NC)"
	git push origin main
	@echo "$(GREEN)✅ Pushed to main$(NC)"

##@ All-in-One

all: clean install-dev lint format test ## Run complete workflow (clean, install, lint, format, test)
	@echo "$(GREEN)✅ All tasks completed successfully!$(NC)"

ci: lint format-check test ## Run CI pipeline (lint, format check, test)
	@echo "$(GREEN)✅ CI pipeline passed!$(NC)"

##@ Information

version: ## Show server version
	@echo "$(BLUE)R2R Ultra MCP Server v3.0$(NC)"
	@echo "FastMCP: $$(fastmcp version | grep 'FastMCP version' | cut -d' ' -f3)"
	@echo "Python: $$(python --version | cut -d' ' -f2)"

env-info: ## Show environment information
	@echo "$(BLUE)Environment Information:$(NC)"
	@echo "Python: $$(which python)"
	@echo "Version: $$(python --version)"
	@echo "FastMCP: $$(fastmcp version | head -1)"
	@echo "Working Dir: $$(pwd)"
	@echo ""
	@echo "$(BLUE)Environment Variables:$(NC)"
	@echo "R2R_BASE_URL: $${R2R_BASE_URL:-not set}"
	@echo "API_KEY: $${API_KEY:+configured}"

##@ Documentation

docs: ## Open documentation in browser
	@echo "$(BLUE)📚 Opening documentation...$(NC)"
	@open README.md || xdg-open README.md || echo "$(YELLOW)Please open README.md manually$(NC)"

##@ Docker (Future)

docker-build: ## Build Docker image (TODO)
	@echo "$(YELLOW)⚠️ Docker support coming soon$(NC)"

docker-run: ## Run Docker container (TODO)
	@echo "$(YELLOW)⚠️ Docker support coming soon$(NC)"

