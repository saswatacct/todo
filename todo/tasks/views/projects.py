from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from todo.tasks.models import Project


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "tasks/project/list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return self.request.user.projects.all()
