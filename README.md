# Getting Started

## With Docker

### Create a `.env` file (from `.env.example`) and adjust settings, for example database connection.

```bash
cp .env.example .env
```

### Setup Django app

@todo: Replace `tsm-frontend_web` by real git.ufz.de registry url!!

```bash
docker run --rm --env-file .env tsm-frontend_web migrate
docker run --rm --env-file .env tsm-frontend_web createsuperuser --noinput
docker run --rm --env-file .env tsm-frontend_web loaddata admin_interface_theme_foundation.json
```

### Start Django app in development mode

  ```bash
  docker run --rm --env-file .env -p 127.0.0.1:8000:8000 tsm-frontend_web runserver 0.0.0.0:8000
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
docker-compose run --rm web loaddata admin_interface_theme_foundation.json
```

- open admin frontend at: http://localhost:8000/tsm
- open rest api at: http://localhost:8000/things/

## DjangoTheme Customization
- select the *Foundation* Theme [here](http://localhost:8000/tsm/admin_interface/theme/)
- insert the [UFZ-Logo](admin-interface/logo/UFZ_Logo_SW_RGB_invertiert_DE.png) in the [Theme-Customization-Form](http://localhost:8000/tsm/admin_interface/theme/2/change/), best size is: 
  - Max-width: 400
  - Max-height: 65
- also insert the [UFZ-Favicon](admin-interface/favicon/favicon.ico) in the same form some more at the bottom 
 

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
- Um verschachtelte Formulare zu erstellen (Thing > SftpConfig > Parser):
  - https://github.com/theatlantic/django-nested-admin
