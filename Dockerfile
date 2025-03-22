FROM python:alpine

COPY app /app
WORKDIR /app

RUN rm -rf .env && rm -rf db.sqlite3
COPY requirements.txt requirements.txt
COPY entrypoint.sh /entrypoint.sh

RUN apk update && \
    apk add --no-cache \
        mariadb-dev \
        libffi-dev \
        build-base && \
    pip install -r requirements.txt && \
    apk del \
        build-base && \
    rm -rf /var/cache/apk/*

ENTRYPOINT [ "/entrypoint.sh" ]
EXPOSE 8000/tcp
