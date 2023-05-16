"""capstone2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views as core_views
from friends import views as friends_views
from books import views as book_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home),
    path('join/', core_views.join),
    path('login/', core_views.user_login),
    path('logout/', core_views.user_logout),
    path('FAQ', core_views.FAQ),
    path('feedback', core_views.feedback),
    path('tropes', core_views.Tropes),
    path('view_feedback', core_views.view_feedback),

    path('friends', friends_views.friends),
    path('find_friend', friends_views.find_friend),
    path('send_friend_request/<int:userID>/', friends_views.send_friend_request),
    path('accept_friend_request/<int:requestID>/', friends_views.accept_friend_request),
    path('friend_profile/<int:userID>', friends_views.friend_profile),
    path('remove_friend/<int:userID>', friends_views.remove_friend),

    path('sort', book_views.sorting),
    path('add_book', book_views.add_book),
    path('favorite/<str:title>', book_views.favorite),
    path('view_favorites', book_views.view_favorites),
    path('remove_favorite/<str:title>', book_views.remove_favorite),
    path('rating/<int:bookID>/<int:ratingnum>/', book_views.rating),
]
