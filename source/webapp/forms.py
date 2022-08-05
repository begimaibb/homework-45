import re
from django import forms
from webapp.models import Type, Task, Project
from django.core.exceptions import ValidationError
from django.forms import widgets


class UserTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "type", "project"]


class UserProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "date_started", "date_finished"]


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ["name", "description", "status", "type", "project"]
        widgets = {
            "type": widgets.CheckboxSelectMultiple,
        }

    def clean(self):
        name = self.cleaned_data.get("name")
        description = self.cleaned_data.get("description")
        if not re.match("^[a-zA-Zа-яА-Я\s]+$", name):
            self.add_error("name", ValidationError("The name should include only letters"))
        if not re.match("^[a-zA-Zа-яА-Я\s]+$", description):
            self.add_error("description", ValidationError("The description should include only letters"))
        return super().clean()


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Find')


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ["name", "description", "date_started", "date_finished"]


class TaskDeleteForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name"]

    def clean_title(self):
        name = self.cleaned_data.get("name")
        if self.instance.name != name:
            raise ValidationError("Names do not match")
        return name


class ProjectDeleteForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name"]

    def clean_title(self):
        name = self.cleaned_data.get("name")
        if self.instance.name != name:
            raise ValidationError("Names do not match")
        return name



