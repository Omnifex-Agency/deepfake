# DeepShield AI — ML Experiment Container
FROM python:3.10-slim

# System deps for OpenCV, audio processing, and PDF parsing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsndfile1 \
    ffmpeg \
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

# Run Stage 3 image experiments by default (override as needed)
CMD ["python", "experiments/image/train_and_evaluate.py"]
