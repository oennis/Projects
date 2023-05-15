from django.db import models
from django.conf import settings

# Create your models here.
class Feedback(models.Model):
    user = models.CharField(max_length = 80, default = 'NULL')
    subject = models.CharField(max_length = 80)
    email = models.CharField(max_length = 80)
    feedback = models.CharField(max_length = 400)
