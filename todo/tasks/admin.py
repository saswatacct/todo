from django.contrib import admin

from .models import Project, Task


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    fields = ("description", "deadline")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    list_filter = ("user",)
    search_fields = ("name",)
    ordering = ("name",)
    inlines = (TaskInline,)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("description", "project", "priority", "complete")
    list_filter = ("project", "complete")
    search_fields = ("description",)
    ordering = ("project", "priority")
    readonly_fields = ("priority",)
