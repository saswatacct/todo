from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    complete = models.BooleanField(default=False)
    description = models.TextField()
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.PositiveIntegerField(null=True, blank=True)

    def set_priority(self, new_priority: int) -> None:
        """Set the priority of the task.

        Args:
            new_priority (int): The new priority of the task.
        """

        # Get the current priority of the task
        current_priority = self.priority

        # If the new priority is the same as the current priority, return
        if new_priority == current_priority:
            return

        # Get the tasks in the project
        tasks = Task.objects.filter(project=self.project)

        # If the new priority is greater than the current priority
        if new_priority > current_priority:
            # Update the priority of the tasks between the current priority and the new priority
            tasks.filter(
                priority__gt=current_priority,
                priority__lte=new_priority,
            ).update(priority=models.F("priority") - 1)
        # If the new priority is less than the current priority
        else:
            # Update the priority of the tasks between the new priority and the current priority
            tasks.filter(
                priority__gte=new_priority,
                priority__lt=current_priority,
            ).update(priority=models.F("priority") + 1)

        # Update the priority of the task
        self.priority = new_priority
        self.save()

    def save(self, *args, **kwargs):
        if self.priority is None:
            self.priority = Task.objects.filter(project=self.project).count() + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description[:18]

    class Meta:
        ordering = [
            models.F("priority").asc(nulls_last=True),  # NULL items come last,
            "id",
        ]
