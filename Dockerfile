# DeepShield AI — Production Inference Container
FROM python:3.10-slim

# Install system dependencies for OpenCV and audio processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsndfile1 \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY app/ ./app/
COPY experiments/ ./experiments/
COPY docs/ ./docs/
COPY research/ ./research/

# Expose standard API & UI port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Launch production server
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
