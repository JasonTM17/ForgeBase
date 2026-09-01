from django.urls import path

from common import views

urlpatterns = [
    path("health", views.health),
    path("health/live", views.liveness),
    path("health/ready", views.readiness),
]
