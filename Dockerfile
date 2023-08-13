FROM python:alpine

COPY app /app
# COPY .env.example /app/.env

WORKDIR /app

# RUN apk update && \
#         apk add --no-cache \
#             gcc \
#             musl-dev \
#             pkgconfig \
#             mariadb-dev \
#             build-base \


RUN apk update && \
    apk add --no-cache \
        mariadb-dev \
        build-base

RUN pip install mysqlclient \
    pip install -r requirements.txt && \
    pip install gunicorn mysqlclient

CMD gunicorn -b 0.0.0.0:8000 moneyapp.wsgi
