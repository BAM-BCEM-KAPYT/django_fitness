from django.db import models


class Group(models.Model):
    clients_count = models.IntegerField()
    title = models.CharField(max_length=50)


class Client(models.Model):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    fio = models.CharField(max_length=50)
    classes = models.IntegerField()
