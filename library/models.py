# from django.db import models
import os

from djongo import models


# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=16)

    def __str__(self):
        return self.username, self.password


def upload_path(instance, filename):
    # change the filename here is required
    return os.path.join("uploads", filename)


class ImageModel(models.Model):
    image = models.ImageField(upload_to=upload_path, null=False, blank=True)
    created_date = models.DateTimeField(null=False, blank=True, auto_now_add=True)

