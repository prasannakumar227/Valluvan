from django.db import models
import hashlib
import datetime
import os
from functools import partial

# Create your models here.

def _update_filename(instance, filename, path):
    path = path
    filename = "toProcessImage.jpg"

    return os.path.join(path, filename)


def upload_to(path):
    return partial(_update_filename, path=path)


class image(models.Model):
   img = models.ImageField(upload_to=upload_to("images"))

