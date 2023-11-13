from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeMapView.as_view(), name="map_view"),
    path('add-point', views.AddPointMapView.as_view(), name="add_point_map_view"),
    path('update-point', views.UpdatePointMapView.as_view(), name="update_point_map_view"),
    path('delete-point', views.DeletePointMapView.as_view(), name="delete_point_map_view"),
]