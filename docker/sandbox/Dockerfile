# hiresense-ai/docker/sandbox/Dockerfile
# ============================================================
# HireSense_AI — Gradio Sandbox Dockerfile
# ============================================================

FROM python:3.14-slim

LABEL maintainer="HireSense_AI"
LABEL description="Gradio sandbox for HireSense_AI"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy sandbox requirements
COPY sandbox/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy sandbox app
COPY sandbox/app.py ./app.py

# Copy logo if exists
COPY sandbox/Golden_Heart_AI.jpg ./Golden_Heart_AI.jpg

# Copy outputs
COPY outputs/ ./outputs/

# Environment
ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

# Expose Gradio port
EXPOSE 7860

CMD ["python", "app.py"]