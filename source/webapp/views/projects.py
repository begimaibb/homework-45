from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.utils.http import urlencode

from webapp.forms import TaskForm, SearchForm, ProjectForm
from webapp.models import Task, Project
from django.views.generic import TemplateView, ListView, DetailView, CreateView


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
        return context


class CreateProjectView(CreateView):
    form_class = ProjectForm
    template_name = "projects/create.html"

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        form.instance.project = project
        print(form.instance)
        return super().form_valid(form)