from django import forms

from todo.tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["description", "deadline"]
        widgets = {
            "description": forms.TextInput(attrs={"placeholder": "Start typing here to create new task..."}),
            "deadline": forms.DateInput(attrs={"type": "datetime-local"}),
        }
