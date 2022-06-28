from django.contrib import admin

# Register your models here.
from webapp.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'status', 'date']
    list_display_links = ['name']
    list_filter = ['date']
    search_fields = ['name', 'description']
    fields = ['name', 'description', 'status', 'date']


admin.site.register(Task, TaskAdmin)