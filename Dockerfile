# builder stage: install Python deps
FROM python:3.10-slim AS builder
WORKDIR /install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

# runtime stage
FROM python:3.10-slim
ENV TZ=UTC
RUN apt-get update && apt-get install -y cron && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy installed packages
COPY --from=builder /install /usr/local

# copy app sources
COPY . /app

# ensure directories exist
RUN mkdir -p /data /cron

# install cron file
COPY cron/2fa-cron /etc/cron.d/2fa-cron
RUN chmod 0644 /etc/cron.d/2fa-cron && crontab /etc/cron.d/2fa-cron

EXPOSE 8080

# start cron and uvicorn
CMD service cron start && uvicorn app.main:app --host 0.0.0.0 --port 8080
