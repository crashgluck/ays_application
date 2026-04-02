# Django Deployment Checklist (cPanel / V2 Network)

## 1) Environment variables
Create a `.env` (or equivalent cPanel env config) based on `.env.example` and set:
- `DJANGO_PRODUCTION=1`
- `DJANGO_DEBUG=0`
- `DJANGO_SECRET_KEY` with a strong secret
- `DJANGO_ALLOWED_HOSTS` with your production domains
- `DB_*` and `EMAIL_*` with production credentials

## 2) Install dependencies
```bash
pip install -r requirements.txt
```

## 3) Apply migrations
```bash
python manage.py migrate
```

## 4) Collect static files
```bash
python manage.py collectstatic --noinput
```

## 5) Validate configuration
```bash
python manage.py check --deploy
```

## 6) Restart Passenger
Touch your restart file:
```bash
touch tmp/restart.txt
```

## Notes
- This project now supports local SQLite by default on Windows and remote MySQL for production.
- Report email recipients can be configured through `REPORT_EMAIL_RECIPIENTS`.
- Logging writes to `DJANGO_LOG_FILE`.
