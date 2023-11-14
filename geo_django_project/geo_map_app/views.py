from django.shortcuts import render
from geo_map_app.models import Location
from django.views import View


class HomeMapView(View):

    def get(self, request):
        location = Location.objects.all()

        city = [location_data.lat_lng_data for location_data in location]
        template_name = "map.html"
        return render(request, template_name, {"city_coordinates": city, "template_name": template_name})


class AddPointMapView(View):
    def get(self, request):
        location = Location.objects.all()

        city = [location_data.lat_lng_data for location_data in location]
        template_name = "add_map.html"
        return render(request, template_name, {"city_coordinates": city, "template_name": template_name})


class UpdatePointMapView(View):
    def get(self, request):
        location = Location.objects.all()

        city = [location_data.lat_lng_data for location_data in location]
        template_name = "update_map.html"
        return render(request, template_name, {"city_coordinates": city, "template_name": template_name})

class UpdateCityPointMapView(View):
    def get(self, request, id):
        location = Location.objects.get(id=id)
        city = [location.lat_lng_data]
        template_name = "update_city.html"
        return render(request, template_name, {"city_coordinates": city, "template_name": template_name})


class DeletePointMapView(View):
    def get(self, request):
        location = Location.objects.all()
        city = [location_data.lat_lng_data for location_data in location]
        template_name = "delete_map.html"
        return render(request, template_name, {"city_coordinates": city, "template_name": template_name})
