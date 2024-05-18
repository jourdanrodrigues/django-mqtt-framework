FROM python:3.12.1-alpine

ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /app/

RUN apk add --no-cache gcc musl-dev libffi-dev libmemcached-dev zlib-dev && \
    apk add --no-cache --virtual .build-deps build-base linux-headers && \
    pip install --no-cache-dir --upgrade pip build && \
    apk del .build-deps

ADD setup.py requirements-dev.txt ./

RUN pip install --no-cache-dir -e .[dev]

COPY . .
