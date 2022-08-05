from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

# Create your views here.
from django.utils.http import urlencode

from webapp.forms import TaskForm, SearchForm, UserTaskForm, TaskDeleteForm
from webapp.models import Task
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView, UpdateView


class IndexView(ListView):
    model = Task
    template_name = "tasks/list_of_tasks.html"
    context_object_name = "tasks"
    ordering = "-updated_at"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Task.objects.filter(Q(name__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return Task.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})  # search=dcsdvsdvsd
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class TaskView(TemplateView):
    template_name = "tasks/task_view.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        task = get_object_or_404(Task, pk=pk)
        kwargs["task"] = task
        return super().get_context_data(**kwargs)


class CreateTaskView(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = "tasks/create.html"

    # def form_valid(self, form):
    #     task = form.save(commit=False)
    #     task.save()
    #     form.save_m2m()
    #     return redirect("webapp:project_view", pk=task.pk)


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    form_class = TaskForm
    template_name = "tasks/update.html"
    model = Task

    # def get_form_class(self):
    #     if self.request.GET.get("is_admin"):
    #         return TaskForm
    #     return UserTaskForm


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy('index')
    form_class = TaskDeleteForm

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(data=request.POST, instance=self.get_object())
    #     if form.is_valid():
    #         return self.delete(request, *args, **kwargs)
    #     else:
    #         return self.get(request, *args, **kwargs)