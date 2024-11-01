from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from todo.tasks.models import Task


class PriorityUpdateView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, pk: int, priority: int) -> HttpResponse:
        task: Task = get_object_or_404(Task, pk=pk, project__user=request.user)

        # Ensure the priority is within the bounds of the project's tasks
        if priority < 1:
            task.set_priority(1)
        elif priority > task.project.tasks.count():
            task.set_priority(task.project.tasks.count())
        # If the priority is within the bounds, update it if it has changed
        elif task.priority != priority:
            task.set_priority(priority)

        return HttpResponse(status=204)
