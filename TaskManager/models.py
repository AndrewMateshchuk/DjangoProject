from django.db import models
from django.utils import timezone


class Task(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    priority_choices = (
            ('Высокий', 'Высокий'),
            ('Средний', 'Средний'),
            ('Низкий', 'Низкий'),
    )
    status_choices = (
            ('Выполнено', 'Выполнено'),
            ('В процессе', 'В процессе'),
            ('Не выполнено', 'Не выполнено'),           
    )
    status = models.CharField(
            max_length = 20,
            choices = status_choices,
            default= 'Не выполнено'
    )
    priority = models.CharField(
            max_length = 10,
            choices = priority_choices,
            default= 'Средний'
    )
    created_date = models.DateTimeField(
            default=timezone.now)
    completed_date = models.DateField()

    def complete(self):
        self.status = 'Выполнено'
    def __str__(self):
        return self.title