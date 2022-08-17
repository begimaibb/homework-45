from django.urls import path

from webapp.views.tasks import TaskIndex, TaskView, CreateTask, UpdateTask, DeleteTask
from webapp.views.projects import ProjectIndex, ProjectView, CreateProject, UpdateProject, DeleteProject, ChangeUsersInProject

app_name = "webapp"

urlpatterns = [
    path('tasks/', TaskIndex.as_view(), name="index"),
    path('tasks/add/', CreateTask.as_view(), name="create"),
    path('task/<int:pk>/', TaskView.as_view(), name="task_view"),
    path('task/<int:pk>/update', UpdateTask.as_view(), name="update_task"),
    path('task/<int:pk>/delete', DeleteTask.as_view(), name="delete_task"),
    path('', ProjectIndex.as_view(), name="project_index"),
    path('project/<int:pk>/', ProjectView.as_view(), name="project_view"),
    path('projects/add/', CreateProject.as_view(), name="create_project"),
    path('project/<int:pk>/update', UpdateProject.as_view(), name="update_project"),
    path('project/<int:pk>/delete', DeleteProject.as_view(), name="delete_project"),
    path('projects/<int:pk>/change-users', ChangeUsersInProject.as_view(), name="change_users_in_project"),
]
