from django.contrib import admin

from .models import Task, User


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'title', 'description', 'status', 'created', 'user_id')
    search_fields = ('title',)
    list_filter = ('created',)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username',)
    list_filter = ('is_staff',)


admin.site.register(Task, TaskAdmin)
admin.site.register(User, UserAdmin)
