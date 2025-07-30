from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    name=models.CharField(max_length=50)
    roll=models.IntegerField()
    city=models.CharField(max_length=50)

    def __str__(self):
        return self.name
