from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from books.models import Book
from friends.models import Rating
from core.models import Feedback
from core.forms import JoinForm, LoginForm, FeedbackForm

#Homepage View
@login_required(login_url='/login/')
def home(request):
    book_obj = Book.objects.all()
    favorites = request.user.favorites.all()
    ratings = Rating.objects.filter(user=request.user)
    page_data = {'book_obj':book_obj, 'favorites':favorites, 'ratings':ratings}
    return render(request, 'main/home.html', page_data)

#FAQ page view
@login_required(login_url='/login/')
def FAQ(request):
    return render(request, 'main/FAQ.html')

#Tropes page view
def Tropes(request):
    return render(request, 'main/Tropes.html')

#Admin view of feedback submitted by users
def view_feedback(request):
    feedbacks = Feedback.objects.all()
    page_data = {'feedbacks':feedbacks}
    return render(request, 'main/view_feedback.html', page_data)

#Feedback form submission
@login_required(login_url='/login/')
def feedback(request):
    if (request.method == 'POST'):
        feedback_form = FeedbackForm(request.POST)
        if (feedback_form.is_valid()):
            subject = feedback_form.cleaned_data.get('subject')
            email = feedback_form.cleaned_data.get('email')
            text = feedback_form.cleaned_data.get('feedback')
            Feedback(user=request.user, subject=subject, email=email, feedback=text).save()
            return render(request, 'main/FAQ.html')
        else:
            return render(request, 'main/Feedback.html', {'feedback_form': feedback_form})
    else:
        feedback_form = FeedbackForm()
        return render(request, 'main/Feedback.html', {'feedback_form': feedback_form})

#User login
def user_login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # First get the username and password supplied
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)
            # If we have a user
            if user:
                #Check it the account is active
                if user.is_active:
                    # Log the user in.
                    login(request,user)
                    # Send the user back to homepage
                    return redirect("/")
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return render(request, 'main/login.html', {"login_form": LoginForm})
    else:
        #Nothing has been provided for username or password.
        return render(request, 'main/login.html', {"login_form": LoginForm})

#User Join
def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            # Save form data to DB
            user = join_form.save()
            # Encrypt the password
            user.set_password(user.password)
            # Save encrypted password to DB
            user.save()
            # Success! Redirect to home page.
            return redirect("/")
        else:
            # Form invalid, print errors to console
            page_data = { "join_form": join_form }
            return render(request, 'main/join.html', page_data)
    else:
        join_form = JoinForm()
        page_data = { "join_form": join_form }
        return render(request, 'main/join.html', page_data)

#User Login
@login_required(login_url='/login/')
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return redirect("/")
