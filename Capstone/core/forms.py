from django import forms
from django.core import validators
from friends.models import User
from core.models import Feedback

class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        help_texts = {
        'username': None
        }

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class FeedbackForm(forms.ModelForm):
    subject = forms.CharField(widget=forms.TextInput(attrs={'size': '20'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}))
    feedback = forms.CharField(widget=forms.TextInput(attrs={'size': '128'}))
    class Meta():
        model = Feedback
        fields = ('subject', 'email', 'feedback')
