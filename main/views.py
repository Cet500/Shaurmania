from django.shortcuts import render
from .models import Review, Shaurma


def index( request ):
    shaurma = Shaurma.objects.all()

    ctx = {
        'shaurma': shaurma
    }    
    return render( request, 'main/index.html', context = ctx )

def about( request ):
    return render( request, 'main/about.html' )

def address(request):
    return render(request, 'main/address.html')

def cart(request):
    return render(request, 'main/cart.html')

def catalog(request):
    shaurma = Shaurma.objects.all()

    ctx = {
        'shaurma': shaurma
    }    
    return render( request, 'main/catalog.html', context = ctx )

def feedback(request):
    reviews = Review.objects.all()

    ctx = {
        'reviews': reviews
    }

    return render( request, 'main/feedback.html', context = ctx )

def licenses(request):
    return render(request, 'main/licenses.html')

def login(request):
    return render(request, 'main/login.html')

def product(request):
    return render(request, 'main/product.html')

def reg(request):
    return render(request, 'main/registration.html')

def sales(request):
    return render(request, 'main/sales.html')

def search(request):
    return render(request, 'main/search.html')

def user(request):
    return render(request, 'main/user.html')
