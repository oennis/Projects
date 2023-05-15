from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from friends.models import User, Friend_Request, Rating

# Create your views here.
@login_required(login_url='/login/')
def friends(request):
    user = request.user
    friends = user.friends.all()
    page_data = {'friends':friends}
    return render(request, 'friends/friends_list.html', page_data)

@login_required(login_url='/login/')
def remove_friend(request, userID):
    user = request.user
    friend = User.objects.get(id = userID)
    user.friends.remove(friend)
    friend.friends.remove(user)
    return redirect('/friends')

@login_required(login_url='/login/')
def friend_profile(request, userID):
    friend = User.objects.get(id = userID)
    favorites = friend.favorites.all()
    ratings = Rating.objects.filter(user = userID)
    page_data = {'favorites':favorites, 'friend':friend, 'ratings':ratings}
    return render(request, 'friends/friend_profile.html', page_data)

@login_required(login_url='/login/')
def find_friend(request):
    allusers = User.objects.all()
    user = request.user
    all_friend_requests = Friend_Request.objects.filter(receiver = user)
    page_data = {'allusers':allusers, 'all_friend_requests':all_friend_requests}
    return render(request, 'friends/find_friend.html', page_data)

@login_required(login_url='/login/')
def send_friend_request(request, userID):
    sender = request.user
    receiver = User.objects.get(id = userID)
    friend_request, created = Friend_Request.objects.get_or_create(sender=sender, receiver=receiver)
    if created:
        bool = 'True'
        page_data = {'bool':bool}
        return render(request, 'friends/popup.html', page_data)
    else:
        bool = 'False'
        page_data = {'bool':bool}
        return render(request, 'friends/popup.html', page_data)


@login_required(login_url='/login/')
def accept_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.receiver == request.user:
        friend_request.receiver.friends.add(friend_request.sender)
        friend_request.sender.friends.add(friend_request.receiver)
        friend_request.delete()
        message = 'Friend Request Accepted'
        page_data = {'message':message}
        return redirect('/find_friend.html')
    else:
        message = 'Friend Request Not Accepted'
        page_data = {'message':message}
        return render(request, 'friends/find_friend.html', page_data)
