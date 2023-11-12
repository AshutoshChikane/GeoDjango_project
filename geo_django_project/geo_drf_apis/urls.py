from django.urls import path
from . import views


urlpatterns = [
    path('add_point', views.AddPointView.as_view(), name="map_view")
]