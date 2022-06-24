from django.urls import path
from webapp.views import index_view, create_task


urlpatterns = [
    path('', index_view),
    path('tasks/add/', create_task)
]