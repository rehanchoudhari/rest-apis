import os
from typing import Any
import uuid
from django.db import models
from django.utils.deconstruct import deconstructible

# Create your models here.

class GenerateHouseImagePath(object):
    
    def __init__(self) -> None:
        pass

    def __call__(self, instance, file_name):
        ext = file_name.split('.')[-1]
        path = f'media/houses/{instance.id}/images'
        name = f'main.{ext}'
        return os.path.join(path, name)

image_path = GenerateHouseImagePath

class House(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    image = models.FileField(upload_to=image_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    manager = models.OneToOneField('user.Profile', on_delete=models.SET_NULL, blank=True, null=True, related_name='managed_house')
    points = models.IntegerField(default=0)
    completed_task_count = models.IntegerField(default=0)
    incompleted_task_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id} | {self.name}'