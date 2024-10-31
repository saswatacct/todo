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
