from django.contrib import admin
from .models import User, Friend_Request, Rating

# Register your models here.
admin.site.register(User)
admin.site.register(Rating)
