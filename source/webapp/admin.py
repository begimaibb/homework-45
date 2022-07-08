from django.contrib import admin

# Register your models here.
from webapp.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'status', 'type', 'created_at', 'updated_at']
    list_display_links = ['name']
    list_filter = ['status']
    search_fields = ['name', 'description']
    fields = ['name', 'description', 'status', 'type', 'created_at', 'updated_at']


admin.site.register(Task, TaskAdmin)