FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN --mount=type=cache,id=pip-cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY ml_pipeline.py .

CMD ["python3", "ml_pipeline.py"]
