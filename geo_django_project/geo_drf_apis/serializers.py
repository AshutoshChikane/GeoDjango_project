from rest_framework import serializers
from geo_map_app.models import Location

class MapSerializer(serializers.Serializer):
    class Meta:
        model = Location
        fields = 'point'