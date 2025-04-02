# Define variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
STREAMLIT = $(VENV_DIR)/bin/streamlit

# Set PYTHONPATH dynamically to the absolute path of src/
export PYTHONPATH := $(shell pwd)/

# Default target
all: setup

# Create virtual environment
$(VENV_DIR)/bin/activate: ./requirements.txt
	@echo "Creating virtual environment..."
	@python3 -m venv $(VENV_DIR)
	@$(PIP) install --upgrade pip
	@$(PIP) install -r ./requirements.txt
	@echo "Virtual environment created and packages installed."

# Run Python script with PYTHONPATH
run:
	@echo "Running flow.py with PYTHONPATH=$(PYTHONPATH)"
	@$(STREAMLIT) run src/app/streamlit_app/streamlit_app.py
#	@$(PYTHON) src/app/app.py

# Clean up virtual environment
clean:
	@echo "Removing virtual environment..."
	@rm -rf $(VENV_DIR)
	@echo "Virtual environment removed."

# Setup target to create venv and install packages
setup: $(VENV_DIR)/bin/activate

# Phony targets
.PHONY: all clean setup run
