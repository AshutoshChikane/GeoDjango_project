from django.contrib import admin

from django.contrib.gis.admin import OSMGeoAdmin
from .models import Location

@admin.register(Location)
class LocationAdmin(OSMGeoAdmin):
    default_lat = 4411618
    default_lon = -10940608
    default_zoom = 4
    list_display = ('id', 'city', 'temperature_url',)
