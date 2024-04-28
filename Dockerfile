FROM python:3.12.1-alpine

WORKDIR /app/

RUN pip install --no-cache-dir --upgrade pip wheel

ADD setup.py .

RUN pip install -e . djangorestframework>=3.15 pydantic>=2.7.1

COPY . .
