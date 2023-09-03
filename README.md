# MoneyApp

This is a semi serious app to try real world deployments of several technologies
including Open Telemetry, HoneyComb, ECS and more.

## Development

```python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

```
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

## Docker Dev Environment

Build
```bash
docker build . -t moneyapp:latest
# or
docker-compose build
```

Run
```bash
docker-compose up -d
```

Migrate
```bash
docker-compose exec web python manage.py migrate
```

## Running an OpenTelemetry Collector

```bash
cp opentelemetry.config.yaml.example opentelemetry.config.yaml
```

Included in [docker-compose.yml](docker-compose.yml). Or run it manually

```bash
docker run \
    -p 4317:4317 \
    -v ./opentelemetry.config.yaml:/etc/otel-collector-config.yaml \
    otel/opentelemetry-collector:latest \
    --config=/etc/otel-collector-config.yaml
```

