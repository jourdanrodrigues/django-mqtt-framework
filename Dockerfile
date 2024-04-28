FROM python:3.12.1-alpine

WORKDIR /app/

RUN apk add --no-cache gcc musl-dev libffi-dev libmemcached-dev zlib-dev && \
    apk add --no-cache --virtual .build-deps build-base linux-headers && \
    pip install --no-cache-dir --upgrade pip wheel && \
    apk del .build-deps

ADD setup.py .

RUN pip install -e . djangorestframework>=3.15 pydantic>=2.7.1 django-cache-url>=3.4.5 pylibmc>=1.6.3

COPY . .
