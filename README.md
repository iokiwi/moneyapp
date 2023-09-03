# MoneyApp

## Development

```python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```
## Docker

```bash
docker build . -t moneyapp:latest
# or
docker-compose build
```

```bash
docker-compose up -d
```

```bash
docker-compose exec web python manage.py migrate
```

## Running an OpenTelemetry Collector

```bash
cd app

docker run \
    -p 4317:4317 \
    -v ./opentelemetry.config.yaml:/etc/otel-collector-config.yaml \
    otel/opentelemetry-collector:latest \
    --config=/etc/otel-collector-config.yaml
```
