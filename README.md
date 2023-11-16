# GeoDjango_project
GeoDjango project to map the weather condition for united states and create leaflet view for client

step to follow to run project
1. python -m venv venv
2. venv/script/activate
3. pip install -r requirement.txt
4. pipwin gdal
5. python manage.py makemigrations
6. python manage.py migrate
7. python manage.py runserver

http://127.0.0.1:8000/geo_django_map/ MAP view


1. DRF APIs are render in geo_drf_apis APP
2. MAP-UI view are render in geo_map_app APP

Inside MAP UI 
1. POST drf API is used to store new location
2. PUT drf API is used for updating location
3. DELETE drf API is used to delete location
