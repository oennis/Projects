from django.db import models
from django.contrib.auth.models import User, AbstractUser
from books.models import Book

# Create your models here.
class User(AbstractUser):
    friends = models.ManyToManyField("User", blank = True)
    favorites = models.ManyToManyField(Book, blank = True)

class Friend_Request(models.Model):
    sender = models.ForeignKey(User, related_name = 'sender', on_delete = models.CASCADE)
    receiver = models.ForeignKey(User, related_name = 'receiver', on_delete = models.CASCADE)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
