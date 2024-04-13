FROM python:3.12.1-alpine

WORKDIR /app/

RUN apk add -q --no-cache --virtual .build-deps gcc musl-dev libffi-dev jpeg-dev zlib-dev && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir "poetry==1.8.2" && \
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root --no-cache --no-interaction && \
    apk --purge del .build-deps

COPY . .
