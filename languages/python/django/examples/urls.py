from django.urls import path

from examples import views

urlpatterns = [
    path("examples", views.examples_collection),
    path("examples/<int:item_id>", views.get_example),
]
