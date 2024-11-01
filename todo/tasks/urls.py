from django.urls import path

from .views.projects import ProjectListView

app_name = "tasks"

urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
]
