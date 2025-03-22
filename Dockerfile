FROM python:3.12.7-alpine AS BASE


ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apk add --update curl && \
    rm -rf /var/cache/apk/*


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
