from django.contrib.gis.db.models import PointField
from django.contrib.postgres import operations
from django.db import migrations,models
import requests
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver


class Migration(migrations.Migration):
    dependencies = ["Location", "0001_initial"]
    operations = [
        operations.CreateExtension('postgis')
    ]


class Location(models.Model):
    city = models.CharField(max_length=300, blank=True, default="")
    temperature_url = models.URLField(default="", blank=True)
    point = PointField(unique=True)

    @property
    def lat_lng_data(self):
        try:
            return {
                self.id: {
                    "lat_lng": [self.point.y, self.point.x],
                    "city":self.city,
                    "temperature_url":self.temperature_url
                }
            }
        except Exception:
            return None

