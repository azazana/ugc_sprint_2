"""Gunicorn config for FastAPI."""

import multiprocessing

name = "Gunicorn config for FastAPI"

bind = "0.0.0.0:8000"

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 2 + 1
