from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

# Create your views here.
from django.utils.http import urlencode

from webapp.forms import TaskForm, SearchForm, ProjectForm, UserProjectForm, ProjectDeleteForm, ChangeUsersInProjectForm
from webapp.models import Task, Project
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class ProjectIndex(ListView):
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
        id = self.object.id
        print(id)
        context['tasks'] = Task.objects.filter(project_id=id)
        return context


class CreateProject(PermissionRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = "projects/create.html"
    permission_required = "webapp.add_project"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        return response

    def get_success_url(self):
        return reverse("webapp:project_index")



    # def form_valid(self, form):
    #     project = form.save(commit=False)
    #     project.save()
    #     user = Project.user.all()
    #     form.save_m2m()
    #     form.instance.user = user
    #     return super().form_valid(form)
    #
    # def get_success_url(self):
    #     return reverse("webapp:project_index")

    def has_permission(self):
        return self.request.user.has_perm("webapp.add_project")
               # or \
               # self.request.user == self.get_object().user


class UpdateProject(PermissionRequiredMixin, UpdateView):
    form_class = ProjectForm
    template_name = "projects/update.html"
    model = Project

    def has_permission(self):
        return self.request.user.has_perm("webapp.change_project")
    # def get_form_class(self):
    #     if self.request.GET.get("is_admin"):
    #         return ProjectForm
    #     return UserProjectForm


class DeleteProject(PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = "projects/delete.html"
    success_url = reverse_lazy('webapp:index')
    form_class = ProjectDeleteForm

    def has_permission(self):
        return self.request.user.has_perm("webapp.delete_project")

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(data=request.POST, instance=self.get_object())
    #     if form.is_valid():
    #         return self.delete(request, *args, **kwargs)
    #     else:
    #         return self.get(request, *args, **kwargs)


class ChangeUsersInProject(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = "projects/change_users.html"
    permission_required = "webapp.change_users_in_project"
    form_class = ChangeUsersInProjectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["pk"] = self.request.user.pk
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        return response

    # def has_permission(self):
    #     return self.request.user.has_perm("webapp.change_users_in_project") and self.request.user in self.get_object().users.all()

    def get_success_url(self):
        return reverse("webapp:project_index")
