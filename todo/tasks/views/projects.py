from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView

from todo.project.utils.htmx import render_swap
from todo.project.utils.modal import HIDE_MODAL_EVENT, ModalMixin
from todo.tasks.forms import ProjectForm
from todo.tasks.models import Project


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "tasks/project/list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return self.request.user.projects.all()


class ProjectCreateView(LoginRequiredMixin, ModalMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "tasks/project/create_modal.html"
    success_url = "/"

    def form_valid(self, form):
        # Set the user of the project to the current user
        form.instance.user = self.request.user

        # Run the parent form_valid method to save the form
        super().form_valid(form)

        # Return the rendered project item template
        # to be swapped into the project list and trigger
        # hide modal event to close the modal.
        return render_swap(
            self.request,
            "tasks/project/item.html",
            context={
                "project": form.instance,
            },
            params={
                "swap": "beforeend",
                "target": "[data-project-list]",
                "select": ".card",
            },
            trigger=[HIDE_MODAL_EVENT],
        )
