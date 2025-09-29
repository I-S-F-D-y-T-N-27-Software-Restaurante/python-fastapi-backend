# Python restaurant API Backend
PYTHON = python
VENV = .venv
REQ_LINUX = requirements.txt
REQ_WINDOWS = requirements-windows.txt
MAIN = app.main

.PHONY: help env install run copy-env

help:
	@echo "Available commands:"
	@echo "  make env         - Activate virtual environment"
	@echo "  make install     - Install requirements"
	@echo "  make installw     - Install windows requirements"
	@echo "  make copy-env    - Copy .env.example to .env"
	@echo "  make run         - Run the project"

env:
	@echo "Activate the virtual environment:"
	@echo "Linux/macOS: source $(VENV)/bin/activate"
	@echo "Windows PowerShell: ./venv/Scripts/activate"
	@echo "Windows cmd: .venv\\Scripts\\activate.bat"

install:
	pip install -r $(REQ_LINUX)

installw:
	pip install -r $(REQ_WINDOWS)

copy-env:
	@if [ ! -f .env ]; then cp .env.example .env; fi

run:
	$(PYTHON) -m $(MAIN)
