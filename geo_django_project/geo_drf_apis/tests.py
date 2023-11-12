from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from geo_map_app.models import Location
from django.contrib.gis.geos import Point

class AddPointViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_add_point_view(self):
        data = {'latitude': -97.0, 'longitude': 39.7456}
        response = self.client.post('/geo_django_drf/add-point/', data, format='json')


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Location.objects.count(), 1)

    def test_add_point_view_invalid_coordinates(self):
        data = {'latitude': None, 'longitude': 39.7456}
        response = self.client.post('/geo_django_drf/add-point/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Location.objects.count(), 0)

    def test_add_point_view_existing_location(self):
        data = {'latitude': -97.0, 'longitude': 39.7456}
        response1 = self.client.post('/geo_django_drf/add-point/', data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        response2 = self.client.post('/geo_django_drf/add-point/', data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Location.objects.count(), 1)

# class DeletePointViewTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.location = Location.objects.create(point='POINT(30,40)')
#
#     def test_delete_point_view(self):
#         response = self.client.delete(f'/delete-point/{self.location.id}/')
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Location.objects.count(), 0)
#
#     def test_delete_point_view_nonexistent_id(self):
#         response = self.client.delete('/delete-point/999/')
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Location.objects.count(), 1)
#
# class UpdatePointViewTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.location = Location.objects.create(point='POINT(30 40)')
#
#     def test_update_point_view(self):
#         data = {'latitude': 50.0, 'longitude': 60.0}
#         response = self.client.put(f'/update-point/{self.location.id}/', data, format='json')
#         print(response)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.location.refresh_from_db()
#         self.assertEqual(self.location.point.x, 50.0)
#         self.assertEqual(self.location.point.y, 60.0)
#         # Add more assertions based on your application logic
#
#     def test_update_point_view_invalid_coordinates(self):
#         data = {'latitude': 50.0, 'longitude': None}
#         response = self.client.put(f'/update-point/{self.location.id}/', data, format='json')
#         print(response)
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.location.refresh_from_db()
#         self.assertNotEqual(self.location.point.x, 50.0)
#         self.assertNotEqual(self.location.point.y, None)