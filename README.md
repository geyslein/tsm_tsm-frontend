# Getting Started

## With Docker

### Create a `.env` file (from `.env.example`) and adjust settings, for example database connection.

```bash
cp .env.example .env
```

### Setup Django app

```bash
docker run --rm --env-file .env git.ufz.de:4567/rdm-software/timeseries-management/tsm-frontend/tsm-frontend:latest migrate
docker run --rm --env-file .env git.ufz.de:4567/rdm-software/timeseries-management/tsm-frontend/tsm-frontend:latest createsuperuser --noinput
docker run --rm --env-file .env git.ufz.de:4567/rdm-software/timeseries-management/tsm-frontend/tsm-frontend:latest loaddata admin_interface_theme_foundation.json
```

### Start Django app in development mode

  ```bash
  docker run --rm --env-file .env -p 127.0.0.1:8000:8000 git.ufz.de:4567/rdm-software/timeseries-management/tsm-frontend/tsm-frontend:latest runserver 0.0.0.0:8000
  ```

## With Docker Compose

```bash
# Build container
docker-compose build
# Start database and app container
docker-compose up -d
# Do Djangi migrations
docker-compose run --rm web migrate
# Create Djagno Admin superuser (with credentials from environment vars)
docker-compose run --rm web createsuperuser --noinput
# Load Django fixtures
docker-compose run --rm web loaddata ufz_theme.json
```

- open admin frontend at: http://localhost:8000/tsm
- open rest api at: http://localhost:8000/things/

# Resources
- https://docs.djangoproject.com/en/4.0/
- https://www.django-rest-framework.org/

## Django AdminSite-API and URL patterns
- https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#reversing-admin-urls
- https://docs.djangoproject.com/en/3.2/_modules/django/contrib/admin/sites/

## alternate Django theme
- https://github.com/fabiocaccamo/django-admin-interface
  - Um weiterhin Templates selbst anpassen zu können: https://github.com/bittner/django-apptemplates
  - an die default django themes kommt man z.B. so heran: ``docker cp tsm-frontend-web-1:/usr/local/lib/python3.10/site-packages/django/contrib/admin/templates/admin/base_site.html .`` 
