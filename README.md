


# Getting Started

- docker-compose build
- docker-compose up -d
- docker-compose exec web bash
  - python manage.py migrate
  - python manage.py createsuperuser
  - python manage.py loaddata admin_interface_theme_foundation.json

- open admin frontend at: http://localhost:8000/admin/
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
