# hiresense-ai/docker/ai-service/Dockerfile
# ============================================================
# HireSense_AI — AI Service Dockerfile
# Redrob AI Intelligent Candidate Discovery & Ranking
# ============================================================

FROM python:3.11-slim

LABEL maintainer="HireSense_AI"
LABEL description="AI ranking service for HireSense_AI"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY ai-service/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy AI service source code
COPY ai-service/ ./ai-service/

# Copy outputs folder
COPY outputs/ ./outputs/

# NOTE: chroma_db is NOT copied into image
# It must be mounted at runtime using -v flag:
# -v /path/to/chroma_db:/app/ai-service/chroma_db
# Run index_data.py first to build chroma_db locally

WORKDIR /app/ai-service

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["python", "rank.py"]