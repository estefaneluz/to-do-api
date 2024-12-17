from django.utils import timezone
import pytz
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4

from django.db import models
from users.models import User

class TaskStatus(Enum):
    PENDING = "pending"
    DONE = "done"

class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100, default=str)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name

class TaskItem(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=10, choices=[(status.name, status.value) for status in TaskStatus], default=TaskStatus.PENDING.name)
    is_active = models.BooleanField(default=True)
    tags = models.ManyToManyField('Tag', related_name='tasks', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def update_status(self, status: TaskStatus):
        self.status = status.name
        self.updated_at = timezone.now()

    def update_task(self, title: str = None, tags: List[UUID] = None, status: TaskStatus = None):
        self.status = status.name
        self.updated_at = timezone.now()

        if title:
            self.title = title
        if tags:
            self.tags.set(tags)
        else:
            self.tags.clear()


    def deactivate(self):
        self.is_active = False
        self.deleted_at = datetime.now()
        self.save()

    def __str__(self):
        return self.title