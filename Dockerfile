FROM python:3.8

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir gradient
