FROM python:3.11-slim

WORKDIR /app

COPY microblog/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microblog ./microblog

COPY .env ./
COPY docker-compose.yml ./

COPY frontend ./frontend

CMD ["uvicorn", "microblog.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
