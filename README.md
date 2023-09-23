# MoneyApp

This is a semi serious app to try real world deployments of several technologies
including Open Telemetry, HoneyComb, ECS and more.

## Development

```python
cd moneyapp/app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

```bash
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

## Docker Dev Environment

```bash
cp app/.env.example app/.env
```

Build
```bash
docker-compose build
```

Run
```bash
docker-compose up -d
```

Hot Reload:
 * The app container will reload on code changes

Jaeger UI:
  http://localhost:16686/

APP:
  http://localhost:8000/

<!-- Migrate
```bash
docker-compose exec web python manage.py migrate
``` -->

## Running an OpenTelemetry Collector

```bash
cp otel-collector-config.yaml.example otel-collector-config.yaml
```

Included in [docker-compose.yml](docker-compose.yml). Or run it manually

```bash
docker run \
    -p 4317:4317 \
    -v ./otel-collector-config.yaml:/etc/otel-collector-config.yaml \
    otel/opentelemetry-collector:latest \
    --config=/etc/otel-collector-config.yaml
```

