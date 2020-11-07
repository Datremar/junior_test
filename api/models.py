from django.utils.timezone import now
from django.db import models


class Deal(models.Model):
    username = models.CharField(max_length=64, default='anonymous')
    spent_money = models.IntegerField()
    gem_name = models.CharField(max_length=32, default='none')
    gems = models.IntegerField()
    date = models.DateTimeField(default=now)


class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.title
