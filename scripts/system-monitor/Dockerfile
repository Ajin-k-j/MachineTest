FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (psutil needs gcc on some alpine images, but slim is fine)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY monitor.py .

# Unbuffered output so we can see logs immediately
ENV PYTHONUNBUFFERED=1

CMD ["python", "monitor.py"]