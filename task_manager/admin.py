from django.contrib import admin

from task_manager.models import Position, Project, Task, TaskType, Team, Worker
from django.contrib.auth.admin import UserAdmin


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)


class WorkerAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "team", "position")
    list_filter = ("position",)
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("team", "position")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("team", "position")}),
    )
    ordering = ("position",)


admin.site.register(Worker, WorkerAdmin)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "team", "start_date", "end_date")
    list_filter = ("team",)
    search_fields = ("name", "description")
    date_hierarchy = "start_date"
    ordering = ("start_date",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "deadline",
        "is_complited",
        "task_type",
        "priority",
        "project",
    )
    list_filter = ("task_type", "priority", "is_complited", "project")
    filter_horizontal = ("assignees",)
    search_fields = ("name", "description")
    date_hierarchy = "deadline"
    ordering = ("deadline",)
    actions = ["mark_as_completed"]

    def mark_as_completed(self, request, queryset):
        queryset.update(is_complited=True)

    mark_as_completed.short_description = "Mark selected tasks as completed"
