# Multi-stage build: smaller final image
FROM python:3.10-slim as builder

WORKDIR /app

# Install system dependencies (if any, none needed for this project)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.10-slim

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /root/.local /root/.local

# Ensure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Create data and logs directories
RUN mkdir -p data logs

# Expose ports (FastAPI: 8000, Streamlit: 8501)
EXPOSE 8000 8501

# Default command (can be overridden by docker-compose)
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0"]