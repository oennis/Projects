from django.db import models
from django.conf import settings

#Book model
class Book(models.Model):
    title = models.CharField(max_length = 80)
    author = models.CharField(max_length = 80)
    description = models.CharField(max_length = 500)
    genre1 = models.CharField(max_length = 50)
    genre2 = models.CharField(max_length = 50)
    genre3 = models.CharField(max_length = 50)
    trope1 = models.CharField(max_length = 50)
    trope2 = models.CharField(max_length = 50)
    trope3 = models.CharField(max_length = 50)
