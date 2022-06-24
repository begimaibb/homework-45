from django.shortcuts import render

# Create your views here.
from webapp.models import Task


def index_view(request):
    tasks = Task.objects.order_by("date")
    context = {"tasks": tasks}
    return render(request, "list_of_tasks.html", context)


def create_task(request):
    if request.method == "GET":
        return render(request, "create.html")
    else:
        description = request.POST.get("description")
        status = request.POST.get("status")
        date = request.POST.get("date")
        new_task = Task.objects.create(description=description, status=status, date=date)
        tasks = Task.objects.order_by("date")
        context = {"tasks": tasks}
        return render(request, "list_of_tasks.html", context)
