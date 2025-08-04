# celery_app.py
import os
from celery import Celery

BROKER_URL = os.getenv("CELERY_BROKER_URL", "sqla+sqlite:///./celery_broker.sqlite")
RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "db+sqlite:///./celery_results.sqlite")

celery = Celery(
    "job_processor",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
)

# Optional tuning for SQLite
celery.conf.task_track_started = True
celery.conf.task_ignore_result = False

# Import tasks
celery.conf.imports = ["lib.tasks"]

