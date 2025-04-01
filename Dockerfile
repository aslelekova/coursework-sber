# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY ./api /app/api
COPY ./classification /app/classification
COPY ./detection /app/detection
COPY ./models /app/models
COPY ./data /app/data
COPY ./api/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
