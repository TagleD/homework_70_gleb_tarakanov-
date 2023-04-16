from django.contrib import admin
from webapp.models import Task, Type, Status


# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'status', 'created_at', 'updated_at')
    list_filter = ('id', 'title', 'description', 'status', 'created_at', 'updated_at')
    search_fields = ('id', 'title', 'description', 'status', 'created_at', 'updated_at')
    fields = ('id', 'title', 'description', 'status', 'created_at', 'updated_at')
    readonly_fields = ('id', 'title', 'description', 'status', 'created_at', 'updated_at')


admin.site.register(Task, TaskAdmin)


class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('id', 'name')
    fields = ('id', 'name')
    readonly_fields = ('id', 'name')


admin.site.register(Type, TypeAdmin)


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('id', 'name')
    fields = ('id', 'name')
    readonly_fields = ('id', 'name')


admin.site.register(Status, StatusAdmin)
