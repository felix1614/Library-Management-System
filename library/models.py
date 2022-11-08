# from django.db import models
from djongo import models


# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=16)

    def __str__(self):
        return self.username, self.password

