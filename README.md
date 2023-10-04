# MoneyApp

![flake8](https://github.com/iokiwi/moneyapp/actions/workflows/flake8.yml/badge.svg)
![black](https://github.com/iokiwi/moneyapp/actions/workflows/black.yml/badge.svg)


This is a semi serious app to try real world deployments of several technologies
including Open Telemetry, HoneyComb, ECS and more.

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

The app container will reload on code changes

App:
  http://localhost:8000/

Jaeger UI:
  http://localhost:16686/
