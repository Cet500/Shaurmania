from django.shortcuts import render, redirect
from .models import Review, Shaurma
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LoginForm


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

def product( request, product_id ):
    product = Shaurma.objects.get( id = product_id )
    reviews = Review.objects.filter( shaurma = product_id )

    ctx = {
        'product': product,
        'reviews': reviews
    }

    return render( request, 'main/product.html', context = ctx )

def sales(request):
    return render(request, 'main/sales.html')

def search(request):
    if 'search' in request.GET:
        query = request.GET['search']

        if query:
            finded_rows = Shaurma.objects.filter( name__icontains = query )

            ctx = {
                'search': f'Найдено по запросу "{query}"',
                'finded_rows': finded_rows
            }

        else:
            ctx = {
                'search': 'Пустой запрос, искать нечего'
            }

    else:
        ctx = {
            'search': 'Введите запрос'
        }

    return render( request, 'main/search.html', context = ctx )

def user_private(request):
    return render(request, 'main/user_private.html')

def user_public(request):
    return render(request, 'main/user_public.html')

def reg(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            print('залупень')
            return render(request, 'main/registration.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'main/registration.html', {'form': form})

def login(request):
    return render(request, 'main/login.html')
