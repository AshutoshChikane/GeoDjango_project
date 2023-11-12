from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from geo_map_app.models import Location
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError as DjIntegrityError
from django.db import transaction
from psycopg2.errors import UniqueViolation
from psycopg2 import IntegrityError


class AddPointView(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            latitude = request.data.get("latitude", None)
            longitude = request.data.get("longitude", None)
            if longitude is not None and latitude is not None:

                new_instance = Location(
                    point=Point(x=latitude, y=longitude)
                )
                response = new_instance.save()
                if response == True:
                    response_data = {'detail': "Location created successfully"}
                    return Response(response_data, status.HTTP_200_OK)
                else:
                    response_data = {'detail': "We only present data for united nations"}
                    return Response(response_data, status.HTTP_400_BAD_REQUEST)
            else:
                response_data = {'detail': "Enter Proper Coordinates"}
                return Response(response_data, status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            response_data = {'detail': "Location already exist"}
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        except DjIntegrityError:
            response_data = {'detail': "Location already exist"}
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        except UniqueViolation:
            response_data = {'detail': "Location already exist"}
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        except Exception as exp:
            print(type(exp))
            response_data = {'detail': "internal server error"}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeletePointView(APIView):

    def delete(self, request, id):
        try:
            delete_instance = Location.objects.get(id=id)
            delete_instance.delete()
            response_data = {'detail': f"Location ID: {id} delete successfully"}
            return Response(response_data, status.HTTP_200_OK)
        except ObjectDoesNotExist:
            response_data = {'detail': f"Location ID: {id} does not exist"}
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        except Exception as exp:
            print(exp)
            response_data = {'detail': "internal server error"}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdatePointView(APIView):

    def put(self, request, id):
        try:
            latitude = request.data.get("latitude", None)
            longitude = request.data.get("longitude", None)
            if latitude is not  None and longitude is not None:
                instance = Location.objects.get(id=id)
                instance.point.x = latitude
                instance.point.y = longitude
                instance.city = ""
                instance.gridx = 0
                instance.gridy = 0
                instance.gridId = ""
                instance.save()
                response_data = {'detail': f"object ID: {id} updated successfully"}
                return Response(response_data, status.HTTP_200_OK)
            else:
                response_data = {'detail': "Enter Proper Coordinates"}
                return Response(response_data, status.HTTP_400_BAD_REQUEST)

        except Exception as exp:
            print(exp)
            response_data = {'detail': "internal server error"}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

