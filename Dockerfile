FROM python:latest

RUN mkdir -p /app
WORKDIR /app
EXPOSE 80
EXPOSE 161

RUN set -x \
    && apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    python3-dev

COPY requirements.txt /app

RUN pip install --upgrade pip --no-cache-dir \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -f requirements.txt \
    && apt-get remove -y gcc python3-dev curl \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
