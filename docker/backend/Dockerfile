# hiresense-ai/docker/backend/Dockerfile
# ============================================================
# HireSense_AI — Go Backend Dockerfile
# Gin Framework REST API | Port 8080
# ============================================================

FROM golang:1.26-alpine AS builder

# Metadata
LABEL maintainer="HireSense_AI"
LABEL description="Go backend API for HireSense_AI"

# Set working directory
WORKDIR /build

# Install git for go modules
RUN apk add --no-cache git

# Copy go module files
COPY backend/go.mod backend/go.sum ./

# Download dependencies
RUN go mod download

# Copy backend source code
COPY backend/ .

# Build binary
RUN CGO_ENABLED=0 GOOS=linux go build \
    -o hiresense-backend \
    ./cmd/main.go

# ── Production stage ──
FROM alpine:latest

WORKDIR /app

# Install CA certificates
RUN apk --no-cache add ca-certificates tzdata

# Copy binary from builder
COPY --from=builder /build/hiresense-backend .

# Copy CSV output
COPY outputs/ ./outputs/

# Environment
ENV PORT=8080
ENV ENVIRONMENT=production
ENV CSV_PATH=./outputs/HireSense_AI.csv
ENV ALLOW_ORIGIN=*

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s \
    CMD wget -qO- http://localhost:8080/health || exit 1

# Run backend
CMD ["./hiresense-backend"]