FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for OpenCV and MediaPipe
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port (Hugging Face Spaces uses port 7860)
EXPOSE 7860

# Run the application
# Note: For HF Spaces, you may need to use host 0.0.0.0 and the port from env
# Update app.py to read PORT from environment for HF Spaces compatibility
CMD python -c "import os; from app import app; app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 7860)), debug=False, threaded=True)"

