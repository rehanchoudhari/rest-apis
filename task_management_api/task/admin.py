from django.contrib import admin
from .models import Task, TaskList, Attachment

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class AttachmentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class TaskListAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )

admin.site.register(Task, TaskAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(TaskList, TaskListAdmin)
