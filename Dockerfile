# Dockerfile
# ============================================================
# HireSense_AI — Root Dockerfile
# Full stack: AI Service + Backend + Sandbox
# ============================================================

FROM python:3.14-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc g++ curl wget \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY ai-service/requirements.txt ./requirements-ai.txt
COPY sandbox/requirements.txt    ./requirements-sandbox.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-ai.txt && \
    pip install --no-cache-dir -r requirements-sandbox.txt

# Copy all source
COPY ai-service/ ./ai-service/
COPY sandbox/    ./sandbox/
COPY outputs/    ./outputs/

WORKDIR /app/ai-service

ENV PYTHONUNBUFFERED=1

CMD ["python", "rank.py"]