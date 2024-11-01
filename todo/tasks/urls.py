from django.urls import path

from .views.projects import ProjectListView
from .views.tasks import PriorityUpdateView, TaskCompleteView, TaskCreateView, TaskDeleteView

app_name = "tasks"

# Base urls
urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
]

# Projects HTMX urls
urlpatterns += [
    path("projects/<int:pk>/task-create/", TaskCreateView.as_view(), name="task_create"),
]

# Tasks HTMX urls
urlpatterns += [
    path("tasks/<int:pk>/priority/<int:priority>/", PriorityUpdateView.as_view(), name="task_priority"),
    path("tasks/<int:pk>/complete/", TaskCompleteView.as_view(), name="task_complete"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
]
