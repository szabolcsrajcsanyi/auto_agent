FROM python:3.12.3-slim

WORKDIR /app

COPY src/agents/ ./agents/
COPY src/core/ ./core/
COPY src/memory/ ./memory/
COPY src/schema/ ./schema/
COPY src/service/ ./service/
COPY src/run_service.py .

CMD ["python", "run_service.py"]
