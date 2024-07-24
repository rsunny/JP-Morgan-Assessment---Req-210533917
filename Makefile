.PHONY: install precommit-run precommit-install clean test setup

# Install Python dependencies
install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt

# Install pre-commit hooks
precommit-install:
	@echo "Installing pre-commit hooks..."
	pre-commit install

# Run pre-commit hooks on all files
precommit-run:
	@echo "Running pre-commit hooks on all files..."
	pre-commit run --all-files

# Clean pre-commit environment
clean:
	@echo "Cleaning pre-commit environment..."
	pre-commit clean

# Format code with black, isort, and autoflake
format:
	@echo "Running autoflake..."
	autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive .
	@echo "Running isort..."
	isort .
	@echo "Running black..."
	black .

# Combined command to clean, install hooks, and run pre-commit hooks
setup: clean install precommit-install precommit-run

# Run tests with pytest
test:
	@echo "Running tests with pytest..."
	pytest

# Docker commands
docker-build:
	@echo "Building Docker image..."
	docker build -t gbce-prasanth .

docker-run:
	@echo "Running Docker container..."
	docker run -it --rm gbce-prasanth
