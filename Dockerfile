FROM python:3.11.4-alpine AS BASE

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /dankmemes_bot

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

# TODO: Replace with Makefile
CMD ["sh", "-c", "alembic upgrade head && python3 entrypoint.py"]
