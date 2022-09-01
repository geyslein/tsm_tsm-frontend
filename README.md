


# Getting Started

- docker-compose build
- docker-compose up -d
- docker-compose exec web bash
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py collectstatic --no-input
- python manage.py loaddata admin_interface_theme_foundation.json


- open admin frontend at: http://localhost:8000/admin/
- open rest api at: http://localhost:8000/things/


# Resources
- https://docs.djangoproject.com/en/4.0/
- https://www.django-rest-framework.org/

## alternate Django theme
- https://github.com/fabiocaccamo/django-admin-interface