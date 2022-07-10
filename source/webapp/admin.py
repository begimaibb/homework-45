from django.contrib import admin

# Register your models here.
from webapp.models import Task, Status, Type


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'status', 'type', 'created_at', 'updated_at']
    list_display_links = ['name']
    list_filter = ['status']
    search_fields = ['name', 'description']
    fields = ['name', 'description', 'status', 'type', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'status_name']
    list_display_links = ['status_name']
    list_filter = ['status_name']
    search_fields = ['status_name']
    fields = ['status_name', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name']
    list_display_links = ['type_name']
    list_filter = ['type_name']
    search_fields = ['type_name']
    fields = ['type_name', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Task, TaskAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Type, TypeAdmin)
