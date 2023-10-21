import uuid
import os
from django.db import models
from django.utils.deconstruct import deconstructible

# Create your models here.

NOT_COMPLETE = 'NC'
COMPLETE = 'C'
INPROGRESS = 'IP'
task_status_list = [(NOT_COMPLETE, 'Not Completed'),
                    (COMPLETE, 'Completed'),
                    (INPROGRESS, 'Inprogress')]

@deconstructible
class GenerateAttachmentFilePath(object):
    def __init__(self):
        pass
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/tasks/{instance.task.id}/attachments'
        name = f'{instance.id}.{ext}'
        return os.path.join(path, name)

attachment_path = GenerateAttachmentFilePath()

class TaskList(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('user.profile', null=True, on_delete=models.SET_NULL, related_name='lists')
    house = models.ForeignKey('house.House', on_delete=models.CASCADE, related_name='lists')
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=task_status_list, default=NOT_COMPLETE,)
    
    def __str__(self):
        return f'{self.id} | {self.name}'

class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('user.profile', null=True, on_delete=models.SET_NULL, related_name='created_tasks')
    completed_by = models.ForeignKey('user.profile', null=True, blank=True, on_delete=models.SET_NULL, related_name='completed_tasks')
    task_list = models.ForeignKey('task.TaskList', on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=task_status_list, default=NOT_COMPLETE)

    def __str__(self):
        return f'{self.id} | {self.name}'
    

class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.FileField(upload_to=attachment_path)
    task = models.ForeignKey('task.Task', on_delete=models.CASCADE, related_name='attachment')

    def __str__(self):
        return f'{self.id} | {self.task}'
