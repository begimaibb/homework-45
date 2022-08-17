from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.forms import MyUserCreationForm, UserChangeForm, ProfileChangeForm


# Create your views here.
from accounts.models import Profile


User = get_user_model()


class RegisterView(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = MyUserCreationForm

    def form_valid(self,form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:index')
        return next_url


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('webapp:project_index')
        else:
            context['has_error'] = True
    return render(request, 'login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('webapp:project_index')


def index(request):
    userlist = User.objects.all()
    return render(request, 'project_index.html', {'users': userlist})


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile.html"
    paginate_by = 6
    paginate_orphans = 0

    def get_context_data(self, **kwargs):
        paginator = Paginator(self.get_object().projects.all(),
                              self.paginate_by,
                              self.paginate_orphans)
        page_number = self.request.GET.get('page', 1)
        page_object = paginator.get_page(page_number)
        context = super().get_context_data(**kwargs)
        context['page_obj'] = page_object
        context['projects'] = page_object.object_list
        context['is_paginated'] = page_object.has_other_pages()
        return context


class ChangeProfileView(UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'

    def has_permission(self):
        return self.request.user.is_superuser or self.request.user == self.get_object()

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)

    def get_success_url(self):
        return reverse('accounts:detail', kwargs={'pk': self.object.pk})


class ChangePasswordView(PasswordChangeView):
    # model = User
    # form_class = PasswordChangeForm
    template_name = "change_password.html"

    # def get_object(self, queryset=None):
    #     return self.request.user

    def get_success_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.request.user.pk})

    # def form_valid(self, form):
    #     result = super().form_valid(form)
    #     update_session_auth_hash(self.request, self.object)
    #     return result