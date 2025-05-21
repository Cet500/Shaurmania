from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, Shaurma, Stock, Location, User
from django.contrib.auth import login as login_django, logout as logout_django, authenticate
from .forms import SignUpForm, LoginForm


def index( request ):
    shaurma = Shaurma.objects.all()
    stocks  = Stock.objects.all()

    ctx = {
        'shaurma': shaurma,
        'stocks': stocks
    }    
    return render( request, 'main/index.html', context = ctx )

def about( request ):
    return render( request, 'main/about.html' )

def address(request):
    locations = Location.objects.all()

    ctx = {
        'locations': locations
    }    

    return render(request, 'main/address.html', context = ctx )

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

def stocks(request):
    stocks = Stock.objects.all()

    ctx = {
        'stocks': stocks
    }    
    return render( request, 'main/stocks.html', context = ctx )

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

def user(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_owner = request.user.is_authenticated and request.user.username == username
    if not is_owner and not profile_user.is_open:
        return redirect('user_closed')
    return render(request, 'main/user.html', {
        'profile_user': profile_user,
        'is_owner': is_owner,
    })

def user_closed(request):
    return render(request, 'main/_parts/user_closed.html')

def reg(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_django(request, user)
            return redirect('index')
        else:
            print('залупень')
            return render(request, 'main/registration.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'main/registration.html', {'form': form})

def login(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None: 
                login_django(request, user)
                return redirect('index')
    return render(request, 'main/login.html', {'form': form})

def logout( request ):
    logout_django(request)
    return redirect('index')

def error_400(request, exception):
    return render(request, 'main/error/400.html', status = 400)

def error_403(request, exception):
    return render(request, 'main/error/403.html', status = 403)

def error_404(request, exception):
    return render(request, 'main/error/404.html', status = 404)

def error_500(request):
    return render(request, 'main/error/500.html', status = 500)
