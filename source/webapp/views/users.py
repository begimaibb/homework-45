from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

# Create your views here.
from django.utils.http import urlencode

from webapp.forms import TaskForm, SearchForm, ProjectForm, UserProjectForm, ProjectDeleteForm
from webapp.models import Task, Project
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from accounts.forms import MyUserCreationForm


class AddUser(PermissionRequiredMixin, CreateView):
    form_class = MyUserCreationForm
    template_name = "users/add_users.html"
    success_url = reverse_lazy('webapp:project_index')
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.filter(projects=self.get_object())
        return context

    def has_permission(self):
        return self.request.user.has_perm("webapp.add_user")


class DeleteUser(PermissionRequiredMixin, DeleteView):
    form_class = MyUserCreationForm

    def has_permission(self):
        return self.request.user.has_perm("webapp.delete_user")