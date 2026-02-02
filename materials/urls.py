from django.urls import path
from . import views

urlpatterns = [
    path("", views.materials_home, name="materials_home"),
    path("upload/", views.upload_material, name="upload_material"),
    path("delete/<int:pk>/", views.delete_material, name="delete_material"),
]
