from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DeleteView, UpdateView, View

from todo.core.utils.htmx import render_swap, reswap
from todo.core.utils.modal import HIDE_MODAL_EVENT, ModalMixin, hide_modal
from todo.tasks.forms import TaskForm
from todo.tasks.models import Project, Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task/create_form.html"
    success_url = "/"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Add the project primary key to the context
        context["project"] = {"pk": self.kwargs["pk"]}
        return context

    def form_valid(self, form):
        # Ensure the project is owned by the user
        project: Project = get_object_or_404(Project, pk=self.kwargs["pk"], user=self.request.user)
        form.instance.project = project

        # Run the parent form_valid method to save the form
        # and ensure that the task form is still valid.
        super().form_valid(form)

        # Return the rendered task item template
        # to be swapped into the project task list
        # and trigger the project clear form event
        # to reset the task form.
        return render_swap(
            self.request,
            "tasks/task/item.html",
            context={
                "task": form.instance,
            },
            params={
                "swap": "beforeend",
                "target": f'[data-task-list="{self.kwargs['pk']}"]',
            },
            trigger={
                "project-clear-form": form.instance.project.pk,
            },
        )


class TaskUpdateView(LoginRequiredMixin, ModalMixin, UpdateView):
    template_name = "tasks/task/update_modal.html"
    model = Task
    form_class = TaskForm
    success_url = "/"

    def get_queryset(self) -> QuerySet[Any]:
        # Filter the queryset to only return tasks
        # that are owned by the user.
        return super().get_queryset().filter(project__user=self.request.user)

    def form_valid(self, form):
        # Run the parent form_valid method to save the form
        super().form_valid(form)

        # Return the rendered task item template
        # to be swapped into the project task list
        # and trigger the hide modal event.
        return render_swap(
            self.request,
            "tasks/task/item.html",
            context={
                "task": form.instance,
            },
            params={
                "target": f'[data-task="{form.instance.pk}"]',
                "select": "li",
            },
            trigger=[HIDE_MODAL_EVENT],
        )


class TaskDeleteView(LoginRequiredMixin, ModalMixin, DeleteView):
    model = Task
    template_name = "tasks/task/delete_modal.html"
    success_url = "/"

    def get_queryset(self) -> QuerySet[Any]:
        # Filter the queryset to only return tasks
        # that are owned by the user.
        return super().get_queryset().filter(project__user=self.request.user)

    def delete(self, *args, **kwargs):
        # Run the parent delete method to delete the task
        response = super().delete(*args, **kwargs)

        # Status code 200 is required by HTMX
        # to delete the task from the DOM
        # See: https://htmx.org/attributes/hx-delete/ for more information.
        response.status_code = 200

        # Return the response with the task item to be removed.
        # Since we are overrding the delete method, we need to
        # manually trigger the hide modal event.
        return hide_modal(
            reswap(
                response,
                {"target": f'[data-task="{self.kwargs["pk"]}"]'},
            ),
            {},
        )


class PriorityUpdateView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, pk: int, priority: int) -> HttpResponse:
        task: Task = get_object_or_404(Task, pk=pk, project__user=request.user)

        # Ensure the priority is greater than 0
        # and is different from the current task priority.
        if priority > 0 and priority != task.priority:
            # Update the task priority
            task.set_priority(priority)

        return HttpResponse(status=204)


class TaskCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Get the task object and toggle the complete status
        task = get_object_or_404(Task, pk=pk, project__user=request.user)
        task.complete = not task.complete
        task.save()

        # Return the task item template to be swapped into the project task list
        return render(
            request,
            "tasks/task/item.html",
            {"task": task},
        )
