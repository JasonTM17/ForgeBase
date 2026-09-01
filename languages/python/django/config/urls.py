"""Root URL configuration plus envelope error handlers."""

from django.urls import include, path

urlpatterns = [
    path("", include("common.urls")),
    path("api/v1/", include("examples.urls")),
]

# Framework-level 404/500 render the same envelope as view-level errors.
handler404 = "common.views.not_found"
handler500 = "common.views.server_error"
