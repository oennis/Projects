from django.db import models
from django.contrib.auth.models import User, AbstractUser
from books.models import Book

#Special user model
class User(AbstractUser):
    friends = models.ManyToManyField("User", blank = True)
    favorites = models.ManyToManyField(Book, blank = True)

#Friend functionality based on https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d
#Friend Request Model
class Friend_Request(models.Model):
    sender = models.ForeignKey(User, related_name = 'sender', on_delete = models.CASCADE)
    receiver = models.ForeignKey(User, related_name = 'receiver', on_delete = models.CASCADE)

#Rating Book Model
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
