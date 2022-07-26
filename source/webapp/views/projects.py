from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.utils.http import urlencode
from django.views import View

# from webapp.base_view import FormView as CustomFormView, ListView as CustomListView
from webapp.forms import TaskForm, SearchForm, ProjectForm
from webapp.models import Task, Project
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from webapp.views.base_view import FormView as CustomFormView


class ProjectIndexView(ListView):
    model = Task
    template_name = "projects/list_of_projects.html"
    context_object_name = "projects"
    ordering = "date_started"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Project.objects.filter(Q(name__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return Project.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class ProjectView(DetailView):
    template_name = "projects/project_view.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.comments.order_by("date_started")
        return context


class CreateProject(View):

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            form = TaskForm()
            return render(request, "project/create.html", {"form": form})
#
    def post(self, request, *args, **kwargs):
        self.task = Task()
        form = TaskForm(data=request.POST)
        if form.is_valid():
            type = form.cleaned_data.pop('type')
            self.task.name = form.cleaned_data.get("name")
            self.task.description = form.cleaned_data.get("description")
            self.task.status = form.cleaned_data.get("status")
            self.task.new_task = Task.objects.create(name=self.task.name, description=self.task.description,
                                                     status=self.task.status)
            self.task.new_task.type.set(type)
            return redirect("task_view", pk=self.task.new_task.pk)
        return render(request, "tasks/create.html", {"form": form})


class CreateProject(CreateView):
    form_class = ProjectForm
    template_name = "projects/create.html"

    def form_valid(self, form):
        project = form.save(commit=False)
        project.save()
        form.save_m2m()
        return redirect("article_view", pk=project.pk)
#
#
# class UpdateTask(View):
#
#     def dispatch(self, request, *args, **kwargs):
#         pk = kwargs.get("pk")
#         self.task = get_object_or_404(Task, pk=pk)
#         return super().dispatch(request, *args, **kwargs)
#
#     def get(self, request, *args, **kwargs):
#         if request.method == "GET":
#             form = TaskForm(initial={
#                 "name": self.task.name,
#                 "description": self.task.description,
#                 "status": self.task.status,
#                 "type": self.task.type.all()
#             })
#             return render(request, "tasks/update.html", {"form": form})
#
#     def post(self, request, *args, **kwargs):
#         form = TaskForm(data=request.POST)
#         if form.is_valid():
#             self.task.name = form.cleaned_data.get("name")
#             self.task.description = form.cleaned_data.get("description")
#             self.task.status = form.cleaned_data.get("status")
#             self.task.type.set(form.cleaned_data.pop("type"))
#             self.task.save()
#             return redirect("task_view", pk=self.task.pk)
#         return render(request, "tasks/update.html", {"form": form})
#
#
# class DeleteTask(View):
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get("pk")
#         self.task = get_object_or_404(Task, pk=pk)
#         return render(request, "tasks/delete.html", {"task": self.task})
#
#     def post(self, request, *args, **kwargs):
#         pk = kwargs.get("pk")
#         self.task = get_object_or_404(Task, pk=pk)
#         self.task.delete()
#         tasks = Task.objects.order_by("name")
#         context = {"tasks": tasks}
#         return render(request, "tasks/list_of_tasks.html", context)
