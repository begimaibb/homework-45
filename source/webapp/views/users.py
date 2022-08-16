from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse

# Create your views here.

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


# class DeleteProjectView(PermissionRequiredMixin, DeleteView):
#     model = Project
#     template_name = "users/delete_user.html"
#     success_url = reverse_lazy('webapp:project_index')
#     form_class = ProjectUserDeleteForm
#
#     def has_permission(self):
#         return self.request.user.has_perm("webapp.delete_user")