.PHONY: help install test run build deploy clean

# Default target
help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run tests"
	@echo "  run        - Run the application locally"
	@echo "  build      - Build Docker image"
	@echo "  deploy     - Deploy with Docker Compose"
	@echo "  clean      - Clean up generated files"
	@echo "  format     - Format code with black"
	@echo "  lint       - Run linting with flake8"

# Install dependencies
install:
	pip install -r requirements.txt

# Run tests
test:
	pytest app/tests/ -v

# Run the application locally
run:
	streamlit run app/main.py

# Build Docker image
build:
	docker build -t ai-analytics-app .

# Deploy with Docker Compose
deploy:
	docker-compose up -d

# Stop deployment
stop:
	docker-compose down

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .coverage

# Format code
format:
	black app/ --line-length 88

# Run linting
lint:
	flake8 app/ --max-line-length 88 --ignore E203,W503

# Check code quality
check: format lint test

# Development setup
dev-setup: install
	@echo "Development environment setup complete!"
	@echo "Run 'make run' to start the application"
