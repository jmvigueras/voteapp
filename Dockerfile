FROM python:3.12-slim

WORKDIR /app

# Intall tools for troubleshooting networking issues
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    iputils-ping \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app.run:app"]
