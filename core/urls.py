from django.urls import path
from . import views
from .views import student_dashboard


urlpatterns = [
    path('', views.home, name='home'),
    path("private/", views.private_area, name="private_area"),
    path("staff/", views.staff_dashboard, name="staff_dashboard"),

    path("toggle-registration/", views.toggle_registration, name="toggle_registration"),
    path("student/dashboard/", student_dashboard, name="student_dashboard"),
]

