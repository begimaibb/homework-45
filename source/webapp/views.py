from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views import View

from webapp.forms import TaskForm
from webapp.models import Task
from django.views.generic import TemplateView


class IndexView(View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.order_by("name")
        context = {"tasks": tasks}
        return render(request, "list_of_tasks.html", context)


class TaskView(TemplateView):
    template_name = "task_view.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        task = get_object_or_404(Task, pk=pk)
        kwargs["task"] = task
        return super().get_context_data(**kwargs)


class CreateTask(View):

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            form = TaskForm()
            return render(request, "create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        self.task = Task()
        form = TaskForm(data=request.POST)
        if form.is_valid():
            self.task.name = form.cleaned_data.get("name")
            self.task.description = form.cleaned_data.get("description")
            self.task.status = form.cleaned_data.get("status")
            self.task.type = form.cleaned_data.get("type")
            self.task.new_task = Task.objects.create(name=self.task.name, description=self.task.description,
                                                     status=self.task.status, type=self.task.type)
            return redirect("task_view", pk=self.task.new_task.pk)
        return render(request, "create.html", {"form": form})


class UpdateTask(View):

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        self.task = get_object_or_404(Task, pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            form = TaskForm(initial={
                "name": self.task.name,
                "description": self.task.description,
                "status": self.task.status,
                "type": self.task.type
            })
            return render(request, "update.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            self.task.name = form.cleaned_data.get("name")
            self.task.description = form.cleaned_data.get("description")
            self.task.status = form.cleaned_data.get("status")
            self.task.type = form.cleaned_data.get("type")
            self.task.save()
            return redirect("task_view", pk=self.task.pk)
        return render(request, "update.html", {"form": form})


class DeleteTask(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        self.task = get_object_or_404(Task, pk=pk)
        return render(request, "delete.html", {"task": self.task})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        self.task = get_object_or_404(Task, pk=pk)
        self.task.delete()
        tasks = Task.objects.order_by("name")
        context = {"tasks": tasks}
        return render(request, "list_of_tasks.html", context)
