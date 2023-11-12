from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from geo_map_app.models import Location
from django.contrib.gis.geos import Point


class AddPointView(APIView):
    def post(self,request):
        print(request.data)
        serializers_data = serializers.MapSerializer(data=request.data)
        if serializers_data.is_valid():
            new_instance = Location(
                point=Point(x=request.data["point"]["x"], y=request.data["point"]["y"])
            )
            new_instance.save()

            return Response(serializers_data.data, status.HTTP_200_OK)
        return Response(serializers_data.data, status.HTTP_400_BAD_REQUEST)

