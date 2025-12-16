FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY simulator.py .

# Unbuffered output to ensure logs appear immediately in Docker
ENV PYTHONUNBUFFERED=1

CMD ["python", "simulator.py"]