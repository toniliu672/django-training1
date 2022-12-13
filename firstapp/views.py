from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as authlogin
from django.contrib.auth import logout as authlogout
from django.contrib import messages
from .models import Book
from .forms import BookCreate




# Create your views here.
def index(request):
    return render(request, 'index.html', )

def library(request):
    shelf = Book.objects.all()
    return render(request, 'library.html', {'shelf': shelf})

def upload(request):
    upload = BookCreate()
    if request.method == 'POST':
        upload = BookCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('library')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'upload_form.html', {'upload_form':upload})

def update_book(request, book_id):
    book_id = int(book_id)
    try:
        book_sel = Book.objects.get(id = book_id)
    except Book.DoesNotExist:
        return redirect('library')
    book_form = BookCreate(request.POST or None, instance = book_sel)
    if book_form.is_valid():
       book_form.save()
       return redirect('library')
    return render(request, 'upload_form.html', {'upload_form':book_form})

def delete_book(request, book_id):
    book_id = int(book_id)
    try:
        book_sel = Book.objects.get(id = book_id)
    except Book.DoesNotExist:
        return redirect('index')
    book_sel.delete()
    return redirect('index')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already registered")
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.info(request, "Username already used")
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect('index')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            authlogin(request, user)
            return redirect('library')
        else:
            messages.info(request, 'User are invalid')
            return redirect('login')
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def logout(request):
    authlogout(request)
    return redirect('/')

def detail(request, pk):
    details = Book.objects.get(id=pk)
    return render(request, 'detail.html', {"detail": details})