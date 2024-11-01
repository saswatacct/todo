from django.urls import path

from .views.projects import ProjectCreateView, ProjectDeleteView, ProjectListView, ProjectUpdateView
from .views.tasks import PriorityUpdateView, TaskCompleteView, TaskCreateView, TaskDeleteView, TaskUpdateView

app_name = "tasks"

# Base urls
urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
]

# Projects HTMX urls
urlpatterns += [
    path("projects/<int:pk>/task-create/", TaskCreateView.as_view(), name="task_create"),
    path("projects/<int:pk>/update/", ProjectUpdateView.as_view(), name="project_update"),
    path("projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"),
    path("projects/create/", ProjectCreateView.as_view(), name="project_create"),
]

# Tasks HTMX urls
urlpatterns += [
    path("tasks/<int:pk>/priority/<int:priority>/", PriorityUpdateView.as_view(), name="task_priority"),
    path("tasks/<int:pk>/complete/", TaskCompleteView.as_view(), name="task_complete"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task_update"),
]
