FROM python:alpine

COPY app /app
COPY entrypoint.sh /entrypoint.sh

WORKDIR /app

RUN apk update && \
    apk add --no-cache \
        mariadb-dev \
        build-base && \
    pip install -r requirements.txt && \
    apk del \
        build-base && \
    rm -rf /var/cache/apk/*

ENTRYPOINT [ "/entrypoint.sh" ]
