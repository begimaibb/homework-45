from django.urls import path
from webapp.views import index_view, create_task, task_view


urlpatterns = [
    path('', index_view, name="index"),
    path('tasks/add/', create_task, name="create"),
    path('task/<int:pk>/', task_view, name="task_view")
]