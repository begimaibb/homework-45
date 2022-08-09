from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', required=True, strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirm password', required=True, strip=False, widget=forms.PasswordInput)
    first_name = forms.CharField(label='First name', required=False)
    last_name = forms.CharField(label='Last name', required=False)
    email = forms.EmailField(label='Email', required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if first_name == '' or last_name == '':
            self.add_error("first_name", ValidationError("Your name or last name is blank"))
        if password != password_confirm:
            self.add_error('password',  ValidationError("Passwords do not match"))
        return super().clean()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']