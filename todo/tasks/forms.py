from crispy_forms.helper import FormHelper
from django import forms

from todo.tasks.models import Task


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # Disable the form tag to use the form with htmx
        self.helper.form_tag = False

    class Meta:
        model = Task
        fields = ["description", "deadline"]
        widgets = {
            "description": forms.TextInput(attrs={"placeholder": "Enter a task description"}),
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
