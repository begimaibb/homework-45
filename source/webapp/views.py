from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.urls import reverse
# Create your views here.

from webapp.models import Task


def index_view(request):
    tasks = Task.objects.order_by("date")
    context = {"tasks": tasks}
    return render(request, "list_of_tasks.html", context)

def task_view(request, **kwargs):
    pk = kwargs.get("pk")
    task = get_object_or_404(Task, pk=pk)
    return render(request, "task_view.html", {"task": task})

def create_task(request):
    if request.method == "GET":
        return render(request, "create.html")
    else:
        name = request.POST.get("name")
        description = request.POST.get("description")
        status = request.POST.get("status")
        date = request.POST.get("date")
        new_task = Task.objects.create(name=name, description=description, status=status, date=date)
        tasks = Task.objects.order_by("date")
        context = {"tasks": tasks}
        return render(request, "list_of_tasks.html", context)
