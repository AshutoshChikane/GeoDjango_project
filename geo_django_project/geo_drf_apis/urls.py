from django.urls import path
from . import views


urlpatterns = [
    path('add-point/', views.AddPointView.as_view(), name="add-point"),
    path('delete-point/<int:id>/', views.DeletePointView.as_view(), name="delete-point"),
    path('update-point/<int:id>/', views.UpdatePointView.as_view(), name="update-point")
]