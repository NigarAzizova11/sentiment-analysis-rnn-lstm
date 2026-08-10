FROM python:3.11-slim

WORKDIR /app

# Sistem
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# elaqeler
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY assignment11/sentiment_app/ .

# Render/Railway PORT env-i avtomatik verir, Flask 0.0.0.0-da işləməlidir
ENV PORT=8080
EXPOSE 8080

CMD gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120
