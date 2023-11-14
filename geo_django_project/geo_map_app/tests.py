from django.test import TestCase
from django.contrib.gis.geos import Point
from geo_map_app.models import Location, fetch_data_national_weather_service
from rest_framework.test import APIClient
from rest_framework import status


class MapViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {'latitude': -97.0, 'longitude': 39.7456}
        self.location = Location(point=Point(x=-101, y=40))
        self.location.save()

    def test_get_map_view(self):
        response = self.client.get('/geo_django_map/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_add_view(self):
        response = self.client.get('/geo_django_map/add-point')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_update_view(self):
        response = self.client.get('/geo_django_map/update-point')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_update_city_view(self):
        response = self.client.get(f'/geo_django_map/update-point/{self.location.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_delete_view(self):
        response = self.client.get('/geo_django_map/delete-point')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_save_invalid_location(self):
        response = fetch_data_national_weather_service(-1000, 2000)
        self.assertEqual(response, None)
        location = Location(point=Point(x=-1000, y=2000))
        response = location.save()
        print(response)
