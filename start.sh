#!/bin/bash

# Anzahl der Worker-Prozesse (oft 2 * CPU-Kerne + 1)
WORKERS=${WORKERS:-4} # Standard auf 4, kann per Umgebungsvariable überschrieben werden

# Host und Port, auf dem der Server lauscht
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}

echo "Starting Gunicorn with $WORKERS workers on $HOST:$PORT"

# Startet Gunicorn mit Uvicorn-Workern
gunicorn app.main:app \
  --workers "$WORKERS" \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind "$HOST:$PORT" \
  --log-level info
  #--reload   # option ONLY for development


