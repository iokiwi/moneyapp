FROM python:alpine

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin

# Download the latest installer
RUN apk add curl
ADD https://astral.sh/uv/install.sh /uv-installer.sh
# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

COPY app /app
WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY requirements.txt requirements.txt
COPY entrypoint.sh /entrypoint.sh

RUN apk update && \
    apk add --no-cache \
        mariadb-dev \
        libffi-dev \
        build-base && \
    uv sync && \
    apk del \
        build-base && \
    rm -rf /var/cache/apk/*

ENTRYPOINT [ "/entrypoint.sh" ]
