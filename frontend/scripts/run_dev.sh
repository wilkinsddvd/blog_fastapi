#!/usr/bin/env bash
set -e

if [ ! -f .env ]; then
    cp .env.example .env
fi

pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000