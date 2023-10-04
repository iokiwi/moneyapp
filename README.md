# MoneyApp

![Python Code Style](https://github.com/iokiwi/moneyapp/actions/workflows/code-style.yml/badge.svg)

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
  * http://localhost:8000/

Jaeger UI:
  * http://localhost:16686/

## Contributing

All contributions should be formatted with black and flake8. This will be checked and enforced with CI/CD checks on pull requests.

 * [Black - The uncompromising code formatter.](https://pypi.org/project/black/)
 * [Flake8 - the modular source code checker](https://pypi.org/project/flake8/)

Its recommended to install both of on your local workstation and either run them manually before pushing or
have your IDE/editor run them automatically.

```bash
pip install -r app/requirements-dev.txt
```
