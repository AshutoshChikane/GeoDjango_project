from django.urls import path
from . import views


urlpatterns = [
    path('add_point', views.AddPointView.as_view(), name="add_point_view"),
    path('delete_point/<int:id>/', views.DeletePointView.as_view(), name="delete_point_view"),
    path('update_point/<int:id>/', views.UpdatePointView.as_view(), name="update_point_view")
]