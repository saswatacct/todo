from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Project(models.Model):
    """
    Stores the details of a project that belongs to a user. The
    project can have multiple tasks associated with it.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Stores the details of a task that belongs to a project. The
    task can be marked as complete or incomplete. The task can
    have a description, deadline, and priority.
    """

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
        """
        Override the save method to set the priority of the task
        if it is not provided. The priority is set to the total
        number of tasks in the project + 1.
        """

        if self.priority is None:
            self.priority = Task.objects.filter(project=self.project).count() + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description[:18]

    class Meta:
        ordering = [
            # Since we are using null=True and blank=True for the priority field,
            # but setting the priority in the save method, we don't need to ensure
            # that the null values are sorted last. We can just sort by the priority
            # field in ascending order.
            "priority",
            # As a fallback, we can sort by the id of the task to ensure a consistent order.
            "id",
        ]
