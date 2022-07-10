from django import forms
from django.forms import widgets
from webapp.models import Status
from webapp.models import Type


class TaskForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, label='Name')
    description = forms.CharField(max_length=100, required=True, label='Description',
                                  widget=widgets.Textarea(attrs={"cols": 40, "rows": 3}))
    status = forms.ModelChoiceField(queryset=Status.objects.all())
    type = forms.ModelChoiceField(queryset=Type.objects.all())
