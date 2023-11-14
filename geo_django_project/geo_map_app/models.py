from django.contrib.gis.db.models import PointField
from django.contrib.postgres import operations
from django.db import migrations,models
import requests



class Migration(migrations.Migration):
    dependencies = []
    # dependencies = ["Location", "0001_initial"]
    operations = [
        operations.CreateExtension('postgis')
    ]


class Location(models.Model):
    city = models.CharField(max_length=300, blank=True, default="", unique=True)
    point = PointField(unique=True)
    gridx = models.IntegerField(default=0)
    gridy = models.IntegerField(default=0)
    gridId = models.CharField(default="", blank=True, max_length=10)

    class Meta:
        app_label = 'geo_map_app'

    def save(self, *args, **kwargs):
        response = fetch_data_national_weather_service(self.point.x,self.point.y)
        if response is not None:
            gridx = response.get("gridX", 0)
            gridy = response.get("gridY", 0)
            gridId = response.get("gridId", None)
            city = response["relativeLocation"]["properties"].get("city", None)
            if city is not None and gridx != 0 and gridy != 0 and gridId is not None:
                if self.city == "":
                    self.city = city
                if self.gridx == 0:
                    self.gridx = int(gridx)
                if self.gridy == 0:
                    self.gridy = int(gridy)
                if self.gridId == "":
                    self.gridId = gridId
                super().save(*args, **kwargs)
        # elif self.pk is not None:
        #     self.__class__.objects.filter(pk=self.pk).delete()

    @property
    def lat_lng_data(self):
        return {
            self.id: {
                "lat_lng": [self.point.y, self.point.x],
                "city":self.city,
                "gridX":self.gridx,
                "gridY":self.gridy,
                "gridId":self.gridId
            }
        }


def fetch_data_national_weather_service(longitude, latitude):
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json().get("properties",None)
        if response is not None:
            return response
    return None