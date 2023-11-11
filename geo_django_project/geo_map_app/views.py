from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.gis.geos import Point
from .models import Location
from django.db.models import Q
from django.views import View
import requests

class MapView(View):

    def get(self, request):
        self.update_data_point()
        location = Location.objects.all()

        city = [location_data.lat_lng_data for location_data in location]
        return render(request, "map.html", {"city_coordinates": city})

    def update_data_point(self):
        location = Location.objects.filter(Q(temperature_url="") | Q(city=""))
        for item in location:
            response = self.fetch_data_national_weather_service(item.point.x, item.point.y)
            if response is not None:
                temperature_url = response.get("forecast", None)
                city = response["relativeLocation"]["properties"].get("city", None)
                if temperature_url is not None and city is not None:
                    item.temperature_url = temperature_url
                    item.city = city
                    item.save()
                else:
                    item.delete()

            else:
                item.delete()

    def fetch_data_national_weather_service(self, longitude, latitude):
        url = f"https://api.weather.gov/points/{latitude},{longitude}"
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json().get("properties",None)
            if response is not None:
                print("response")
                return response
        return None
