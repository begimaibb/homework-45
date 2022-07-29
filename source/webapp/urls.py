from django.urls import path

from webapp.views.tasks import IndexView, CreateTaskView, TaskView, UpdateTaskView, DeleteTaskView
from webapp.views.projects import ProjectIndexView, ProjectView, CreateProjectView, UpdateProjectView, DeleteProjectView


urlpatterns = [
    path('tasks/', IndexView.as_view(), name="index"),
    path('tasks/add/', CreateTaskView.as_view(), name="create"),
    path('task/<int:pk>/', TaskView.as_view(), name="task_view"),
    path('task/<int:pk>/update', UpdateTaskView.as_view(), name="update_task"),
    path('task/<int:pk>/delete', DeleteTaskView.as_view(), name="delete_task"),
    path('', ProjectIndexView.as_view(), name="project_index"),
    path('project/<int:pk>/', ProjectView.as_view(), name="project_view"),
    path('projects/add/', CreateProjectView.as_view(), name="create_project"),
    path('project/<int:pk>/update', UpdateProjectView.as_view(), name="update_project"),
    path('project/<int:pk>/delete', DeleteProjectView.as_view(), name="delete_project"),
]
