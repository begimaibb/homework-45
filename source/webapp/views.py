from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.urls import reverse

# Create your views here.
from webapp.forms import TaskForm
from webapp.models import Task
from webapp.validate import task_validate


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
        form = TaskForm()
        print(form)
        return render(request, "create.html", {"form": form})
    else:
        form = TaskForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            status = form.cleaned_data.get("status")
            date = form.cleaned_data.get("date")
            new_task = Task.objects.create(name=name, description=description, status=status, date=date)
            return redirect("task_view", pk=new_task.pk)
        return render(request, "create.html", {"form": form})


def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "GET":
        form = TaskForm(initial={
            "name": task.name,
            "description": task.description,
            "status": task.status,
            "date": task.date
        })
        return render(request, "update.html", {"form": form})
    else:
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task.name = form.cleaned_data.get("name")
            task.description = form.cleaned_data.get("description")
            task.status = form.cleaned_data.get("status")
            task.date = form.cleaned_data.get("date")
            task.save()
            return redirect("article_view", pk=task.pk)
        return render(request, "update.html", {"form": form})


def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "GET":
        pass
    #     return render(request, "delete.html", {"task": task})
    else:
        task.delete()
        return redirect("list_of_tasks")
