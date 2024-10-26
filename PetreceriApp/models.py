
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.IntegerField(primary_key=True, null=False, unique=True)
    name = models.CharField(max_length=50, null=True, unique=True, blank=True)
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(unique=True, max_length=50, blank=True, null=True)
    password = models.CharField(unique=True, null=False, max_length=20)
    parties = models.ManyToManyField('Party', related_name='participants')
    responsibilities = models.ManyToManyField('Tasks', related_name='responsibilities')



class Party(models.Model):
    id = models.IntegerField(primary_key=True, null=False, unique=True)
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=50)
    max_nr_people = models.IntegerField()
    budget_total = models.IntegerField()
    date = models.DateField()
    description = models.TextField(max_length=250, null=True, blank=True)

class Tasks(models.Model):
    id = models.IntegerField(primary_key=True, null=False, unique=True)
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=100)
    person = models.CharField(max_length=50)
    party = models.ForeignKey('Party', on_delete=models.CASCADE)




