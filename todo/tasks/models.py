from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User storage model."""

    first_name = models.CharField('Name', max_length=30)
    last_name = models.CharField(
        'Surname', max_length=100, blank=True, null=True
    )
    username = models.CharField('Username', max_length=100, unique=True)
    password = models.CharField('Password', max_length=150)

    REQUIRED_FIELDS = ['first_name',]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Task(models.Model):
    """Task storage model."""

    NEW = 'New'
    PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    STATUS_CHOICES = (
        (NEW, 'New'), (PROGRESS, 'In Progress'), (COMPLETED, 'Completed')
    )
    title = models.CharField('Title', max_length=200)
    description = models.TextField('Description', null=True, blank=True)
    status = models.CharField(
        'Status', max_length=20, choices=STATUS_CHOICES, default=NEW)
    created = models.DateTimeField('Creation date', auto_now_add=True)
    user_id = models.ForeignKey(
        User, verbose_name='Author', on_delete=models.CASCADE,
        related_name='tasks')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title
