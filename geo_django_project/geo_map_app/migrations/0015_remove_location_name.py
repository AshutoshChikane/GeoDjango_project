# Generated by Django 4.2.7 on 2023-11-10 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geo_map_app', '0014_alter_location_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='name',
        ),
    ]
