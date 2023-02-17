#!/bin/bash
cd /opt/app
while ! nc -z -v postgres 5432; do
      sleep 1
    done
alembic upgrade head
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
