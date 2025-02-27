from django.urls import include, path

from task_manager.views import (
    CreateProjectView,
    CreateTaskView,
    MessageCreateView,
    PersonalTaskListView, 
    TaskDetailView, 
    TeamProjectListView, 
    TeamProjectTaskListView,
    InboxListView,
    MessageDetailView,
    UpdateProjectView,
    UpdateTaskView,
    DeleteProjectView,
    DeleteTaskView,
)


urlpatterns = [
    path("<str:team_name>/", PersonalTaskListView.as_view(), name="home_page"),
    path("<str:team_name>/projects", TeamProjectListView.as_view(), name="team_projects_list"),
    path("<str:team_name>/projects/create", CreateProjectView.as_view(), name="team_projects_create"),
    path("<str:team_name>/projects/<int:pk_project>/update", UpdateProjectView.as_view(), name="team_project_update"),
    path("<str:team_name>/projects/<int:pk_project>/delete", DeleteProjectView.as_view(), name="team_project_delete"),
    path("<str:team_name>/projects/<int:pk_project>", TeamProjectTaskListView.as_view(), name="team_project_tasks_list"),
    path("<str:team_name>/projects/<int:pk_project>/create", CreateTaskView.as_view(), name="team_project_task_create"),
    path("<str:team_name>/projects/<int:pk_project>/<int:pk_task>/", TaskDetailView.as_view(), name="team_project_task_detail"),
    path("<str:team_name>/projects/<int:pk_project>/<int:pk_task>/update", UpdateTaskView.as_view(), name="team_project_task_update"),
    path("<str:team_name>/projects/<int:pk_project>/<int:pk_task>/delete", DeleteTaskView.as_view(), name="team_project_task_delete"),
    path("<str:team_name>/messages/", InboxListView.as_view(), name="inbox"),
    path("<str:team_name>/messages/create", MessageCreateView.as_view(), name="message_create"),
    path("<str:team_name>/messages/<int:pk_message>/detail", MessageDetailView.as_view(), name="message_detail"),
]


app_name = "task_manager"
