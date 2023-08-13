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
