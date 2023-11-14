from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from geo_map_app.models import Location
from django.contrib.gis.geos import Point
from django.urls import reverse
import unittest.mock


class AddPointViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_add_point_view(self):
        data = {'longitude': -97.0, 'latitude': 39.7456}
        response = self.client.post('/geo_django_drf/add-point/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Location.objects.count(), 1)

    def test_add_point_view_invalid_coordinates(self):
        data = {'latitude': None, 'longitude': 39.7456}
        response = self.client.post('/geo_django_drf/add-point/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Location.objects.count(), 0)

    def test_add_point_view_existing_location(self):
        data = {'longitude': -97.0, 'latitude': 39.7456}
        response1 = self.client.post('/geo_django_drf/add-point/', data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        response2 = self.client.post('/geo_django_drf/add-point/', data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Location.objects.count(), 1)

    def test_add_point_view_out_of_united_state_location(self):
        data = {'longitude': -97.0, 'latitude': 1}
        response = self.client.post('/geo_django_drf/add-point/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Location.objects.count(), 0)

    def test_add_point_view_wrong_invalid_location(self):
        data = {'latitude': -97.0, 'longitude': 1111}
        response = self.client.post('/geo_django_drf/add-point/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Location.objects.count(), 0)

    def test_add_point_view_add_sting_co_ordinate(self):
        data = {'latitude': -97.0, 'longitude': "abc"}
        response = self.client.post('/geo_django_drf/add-point/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(Location.objects.count(), 0)


class DeletePointViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.location = Location(point=Point(x=-101, y=40))
        self.location.save()

    def test_delete_point_view(self):
        response = self.client.delete(f'/geo_django_drf/delete-point/{self.location.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Location.objects.count(), 0)

    def test_delete_point_view_nonexistent_id(self):
        response = self.client.delete('/geo_django_drf/delete-point/999/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Location.objects.count(), 1)

    def test_delete_point_internal_server_error(self):
        with unittest.mock.patch.object(Location, 'delete',
                                        side_effect=Exception('Simulated Internal Server Error')):
            url = reverse('delete-point', kwargs={'id': self.location.id})
            response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdatePointViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.location = Location(point=Point(x=-101, y=40))
        self.location.save()

    def test_update_point_view(self):
        data = {'longitude': -97.0, 'latitude': 39.7456}
        response = self.client.put(f'/geo_django_drf/update-point/{self.location.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.location.refresh_from_db()
        self.assertEqual(self.location.point.x, -97.0)
        self.assertEqual(self.location.point.y, 39.7456)

    def test_update_point_view_invalid_coordinates(self):
        data = {'latitude': 50.0, 'longitude': None}
        response = self.client.put(f'/geo_django_drf/update-point/{self.location.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.location.refresh_from_db()
        self.assertNotEqual(self.location.point.x, 50.0)
        self.assertNotEqual(self.location.point.y, None)

    def test_update_point_view_add_sting_co_ordinate(self):
        data = {'latitude': -97.0, 'longitude': "abc"}
        response = self.client.put(f'/geo_django_drf/update-point/{self.location.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(Location.objects.count(), 1)
        self.assertNotEqual(self.location.point.x, -97.0)
        self.assertNotEqual(self.location.point.y, "abc")
        self.assertEqual(self.location.point.x, -101)
        self.assertEqual(self.location.point.y, 40)

    def test_update_point_view_without_data(self):
        data = {}
        response = self.client.put(f'/geo_django_drf/update-point/{self.location.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_point_view_out_of_united_state_location(self):
        data = {'longitude': -97.0, 'latitude': 1}
        response = self.client.put(f'/geo_django_drf/update-point/{self.location.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Location.objects.count(), 1)

    def test_update_point_view_wrong_invalid_location(self):
        data = {'longitude': -97.0, 'latitude': 1111}
        response = self.client.put(f'/geo_django_drf/update-point/{self.location.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Location.objects.count(), 1)

    def test_update_point_view_wrong_id(self):
        data = {'longitude': -97.0, 'latitude': 39.7456}
        self.assertEqual(Location.objects.count(), 1)
        response = self.client.put(f'/geo_django_drf/update-point/2/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
