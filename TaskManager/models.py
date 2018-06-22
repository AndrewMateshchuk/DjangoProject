from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.conf import settings
import datetime


class Task(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    date = models.DateField()
    PRIORITY_HIGH = 'Высокий'
    PRIORITY_MEDIUM = 'Средний'
    PRIORITY_LOW = 'Низкий'
    PRIORITY_CHOICES = (
        (PRIORITY_HIGH, 'Высокий'),
        (PRIORITY_MEDIUM, 'Средний'),
        (PRIORITY_LOW, 'Низкий'),
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM)
    status = models.BooleanField(default=False)

    def __str__(self):
        return '{} : {}'.format(self.title, self.date)

    def get_absolute_url(self):
        return reverse('task-detail', args=[str(self.id)])
