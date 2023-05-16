from django import forms
from django.core import validators
from books.models import Book

#Form to add book only used by Admin
class Add_Book(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    author = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'size': '500'}))
    genre1 = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    genre2 = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    genre3 = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    trope1 = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    trope2 = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    trope3 = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    class Meta():
        model = Book
        fields = ('title', 'author', 'description', 'genre1', 'genre2', 'genre3', 'trope1', 'trope2', 'trope3')

#Form used to sort books
class Sorting_Form(forms.Form):
    GENRES = (
        ('None of these', 'None of these'),
        ('Romance', 'Romance'),
        ('Fantasy', 'Fantasy'),
        ('Horror', 'Horror'),
        ('Gothic', 'Gothic'),
        ('Fiction', 'Fiction'),
        ('Contemporary', 'Contemporary'),
        ('Classics', 'Classics'),
        ('Sci-fi', 'Science Fiction'),
        ("Children's", "Children's"),
        ('YA', 'Young Adult'),
        ('NA', 'New Adult'),
        ('BIPOC', 'BIPOC'),
        ('Drama', 'Drama'),
        ('Mystery', 'Mystery'),
        ('Thriller', 'Thriller'),
        ('HistFic', 'Historical Fiction'),
        ('Dystopian', 'Dystopian'),
        ('Action', 'Action'),
    )
    TROPES = (
        ('None of these', 'None of these'),
        ('Chosen One', 'Chosen One'),
        ('Love Triangle', 'Love Triangle'),
        ('Friends to Lovers', 'Friends to Lovers'),
        ('Enemies to Lovers', 'Enemies to Lovers'),
        ('Love at First Sight', 'Love at First Sight'),
        ('Major Character Death', 'Major Character Death'),
        ('Arranged Marriage', 'Arranged Marriage'),
        ('Slow Burn', 'Slow Burn'),
        ('Found Family', 'Found Family'),
        ('Happy Ending', 'Happy Ending'),
        ('Pregnancy', 'Pregnancy'),
        ('Second Chance', 'Second Chance'),
    )
    genresL = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENRES)
    tropesL = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=TROPES)
    genresD = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENRES)
    tropesD = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=TROPES)
