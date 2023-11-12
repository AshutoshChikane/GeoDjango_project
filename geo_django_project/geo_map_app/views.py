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
        location = Location.objects.filter(Q(city="") | Q(gridx=0)| Q(gridy=0)| Q(gridId=""))
        for item in location:
            response = self.fetch_data_national_weather_service(item.point.x, item.point.y)
            if response is not None:
                gridx = response.get("gridX", 0)
                gridy = response.get("gridY", 0)
                gridId = response.get("gridId", None)
                city = response["relativeLocation"]["properties"].get("city", None)
                if city is not None and gridx != 0 and gridy != 0 and gridId is not None:
                    if item.city == "":
                        item.city = city
                    if item.gridx == 0:
                        item.gridx = int(gridx)
                    if item.gridy == 0:
                        item.gridy = int(gridy)
                    if item.gridId == "":
                        item.gridId = gridId
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
                return response
        return None
