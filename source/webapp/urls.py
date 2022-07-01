from django.urls import path
from webapp.views import index_view, create_task, task_view, update_task, delete_task


urlpatterns = [
    path('', index_view, name="index"),
    path('tasks/add/', create_task, name="create"),
    path('task/<int:pk>/', task_view, name="task_view"),
    path('task/<int:pk>/update', update_task, name="update_task"),
    path('task/<int:pk>/delete', delete_task, name="delete_task"),
]