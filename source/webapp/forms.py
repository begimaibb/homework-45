from django import forms
from django.forms import widgets


class TaskForm(forms.Form):
    status_choices = [('new', 'New'), ('in_progress', 'In progress'), ('done', 'Done')]
    name = forms.CharField(max_length=50, required=True, label='Name')
    description = forms.CharField(max_length=100, required=True, label='Description',
                                  widget=widgets.Textarea(attrs={"cols": 40, "rows": 3}))
    status = forms.CharField(label='Status', widget=forms.Select(choices=status_choices))
    date = forms.DateField(required=False, label='Deadline')
