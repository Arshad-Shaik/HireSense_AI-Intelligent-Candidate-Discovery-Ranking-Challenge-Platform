# hiresense-ai/docker/frontend/Dockerfile
# ============================================================
# HireSense_AI — Gradio Sandbox Dockerfile
# HuggingFace Spaces compatible | Port 7860
# ============================================================

FROM python:3.14-slim

# Metadata
LABEL maintainer="HireSense_AI"
LABEL description="Gradio sandbox for HireSense_AI"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy sandbox requirements
COPY sandbox/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy sandbox app
COPY sandbox/ ./sandbox/

# Copy outputs (HireSense_AI.csv)
COPY outputs/ ./outputs/

# Set working directory
WORKDIR /app/sandbox

# Environment for HuggingFace Spaces
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

# Expose port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s \
    CMD curl -f http://localhost:7860/ || exit 1

# Run Gradio app
CMD ["python", "app.py"]