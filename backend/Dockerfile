FROM python:3.11-slim
WORKDIR /app
COPY ./app /app/app
COPY celery_worker.py /app/celery_worker.py
RUN pip install fastapi uvicorn celery redis psycopg[binary] typesense httpx
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
