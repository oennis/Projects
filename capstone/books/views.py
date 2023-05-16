from django.shortcuts import render, redirect
from django.db.models import Q
from books.forms import Sorting_Form, Add_Book
from books.models import Book
from friends.models import User, Rating

#Sorts books after user submits sorting form
def sorting(request):
    if (request.method == 'POST'):
        sort_form = Sorting_Form(request.POST)
        if (sort_form.is_valid()):
            #Liked genres and tropes
            genresL = sort_form.cleaned_data.get('genresL')
            tropesL = sort_form.cleaned_data.get('tropesL')
            #Disliked genres and tropes
            genresD = sort_form.cleaned_data.get('genresD')
            tropesD = sort_form.cleaned_data.get('tropesD')
            book_obj = Book.objects.filter(title='')
            book_obj1 = Book.objects.filter(title='')
            book_obj2 = Book.objects.filter(title='')
            all_books = Book.objects.all()
            i = 0
            #Filters books by genres and tropes
            while i < len(genresL):
                temp_obj = all_books.filter(genre1=genresL[i]) | all_books.filter(genre2=genresL[i]) | all_books.filter(genre3=genresL[i])
                book_obj1 = book_obj1 | temp_obj
                i = i + 1
            i = 0
            while i < len(tropesL):
                temp_obj = all_books.filter(trope1=tropesL[i]) | all_books.filter(trope2=tropesL[i]) | all_books.filter(trope3=tropesL[i])
                book_obj1 = book_obj1 | temp_obj
                i = i + 1
            i = 0
            while i < len(genresD):
                temp_obj = all_books.filter(genre1=genresD[i])| all_books.filter(genre2=genresD[i]) | all_books.filter(genre3=genresD[i])
                book_obj2 = book_obj2 | temp_obj
                i = i + 1
            i = 0
            while i < len(tropesD):
                temp_obj = all_books.filter(trope1=tropesD[i])| all_books.filter(trope2=tropesD[i]) | all_books.filter(trope3=tropesD[i])
                book_obj2 = book_obj2 | temp_obj
                i = i + 1
            #Excludes disliked genres and tropes
            book_obj = book_obj1.difference(book_obj2)
            #Feed information into webpage
            favorites = request.user.favorites.all()
            ratings = Rating.objects.filter(user=request.user)
            page_data = {'genresL':genresL, 'tropesL':tropesL, 'book_obj':book_obj, 'favorites':favorites, 'ratings':ratings}
            return render(request, 'main/home.html', page_data)
        else:
            return render(request, 'books/sorting.html', {'sort_form': sort_form})
    else:
        sort_form = Sorting_Form()
        return render(request, 'books/sorting.html', {'sort_form': Sorting_Form})

def add_book(request):
    #Adds book to the database
    if (request.method == 'POST'):
        book_form = Add_Book(request.POST)
        if (book_form.is_valid()):
            title = book_form.cleaned_data.get('title')
            author = book_form.cleaned_data.get('author')
            description = book_form.cleaned_data.get('description')
            genre1 = book_form.cleaned_data.get('genre1')
            genre2 = book_form.cleaned_data.get('genre2')
            genre3 = book_form.cleaned_data.get('genre3')
            trope1 = book_form.cleaned_data.get('trope1')
            trope2 = book_form.cleaned_data.get('trope2')
            trope3 = book_form.cleaned_data.get('trope3')
            Book(user=request.user, title=title, author=author, description=description, genre1=genre1, genre2=genre2, genre3=genre3, trope1=trope1, trope2=trope2, trope3=trope3).save()
            return redirect('/')
        else:
            return render(request, 'books/add_book.html', {'book_form': book_form})
    else:
        book_form = Add_Book()
        page_data = {'book_form': book_form}
        return render(request, 'books/add_book.html', page_data)

def view_favorites(request):
    #View the favorite books of the current user
    user = request.user
    favorites = user.favorites.all()
    ratings = Rating.objects.filter(user=request.user)
    page_data = {'favorites':favorites, 'ratings':ratings}
    return render(request, 'books/favorites.html', page_data)

def favorite(request, title):
    #Add a Book to your favorites
    user = request.user
    f_title = title
    book_obj = Book.objects.get(title = f_title)
    user.favorites.add(book_obj)
    return redirect('/')

def remove_favorite(request, title):
    #Remove Book from your favorites
    user = request.user
    f_title = title
    book_obj = Book.objects.get(title = f_title)
    user.favorites.remove(book_obj)
    return redirect('/')

def rating(request, bookID, ratingnum):
    #Give rating to a Book
    book = Book.objects.get(id=bookID)
    Rating.objects.filter(book=book, user=request.user).delete()
    Rating(user=request.user, book=book, rating=ratingnum).save()
    return redirect('/')
