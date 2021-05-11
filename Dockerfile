FROM python:3.8

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir gradient

ENV PAPERSPACE_API_KEY your_api_key_value
ENV PAPERSPACE_WEB_URL https://console.paperspace.com
ENV PAPERSPACE_CONFIG_HOST https://api.paperspace.io
ENV PAPERSPACE_CONFIG_LOG_HOST https://logs.paperspace.io
ENV PAPERSPACE_CONFIG_EXPERIMENTS_HOST https://services.paperspace.io/experiments/v1/
ENV PAPERSPACE_CONFIG_EXPERIMENTS_HOST_V2 https://services.paperspace.io/experiments/v2/
ENV PAPERSPACE_CONFIG_SERVICE_HOST https://services.paperspace.io

ENTRYPOINT ["gradient"]