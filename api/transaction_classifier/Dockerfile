FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY main.py .
COPY test_data.py .

# Expose port
EXPOSE 8000

# Run API
CMD ["python", "main.py"]
