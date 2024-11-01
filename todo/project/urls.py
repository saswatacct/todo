from django.contrib import admin
from django.urls import include, path

# Base urls
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("todo.tasks.urls")),
    path("", include("todo.core.urls")),
]
