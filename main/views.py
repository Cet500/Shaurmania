from django.contrib.auth import login as login_django, logout as logout_django, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Review, Shaurma, Stock, Location, User, ShaurmaImage
from .forms import SignUpForm, LoginForm


def index( request ):
    shaurma = Shaurma.objects.all()
    stocks  = Stock.objects.all()

    ctx = {
        'shaurma': shaurma,
        'stocks': stocks
    }    
    return render( request, 'main/index.jinja', context = ctx )

def about( request ):
    return render( request, 'main/about.jinja' )

def address(request):
    locations = Location.objects.all()
    paginator = Paginator( locations, 5 )

    page_number = request.GET.get( 'page' )
    page_obj = paginator.get_page( page_number )

    ctx = {
        'page_obj': page_obj
    }

    if request.headers.get( 'x-requested-with' ) == 'XMLHttpRequest':
        locations_html = render_to_string( 'main/_parts/locations_list.jinja', ctx, request = request )
        pagination_html = render_to_string( 'main/_parts/pagination.jinja', ctx, request = request )

        return HttpResponse( locations_html + pagination_html )

    return render( request, 'main/address.jinja', context = ctx )

def catalog(request):
    shaurma = Shaurma.objects.all()

    ctx = {
        'shaurma': shaurma
    }    
    return render( request, 'main/catalog.jinja', context = ctx )

def feedback(request):
    reviews = Review.objects.all()
    paginator = Paginator( reviews, 50 )

    page_number = request.GET.get( 'page' )
    page_obj = paginator.get_page( page_number )

    ctx = {
        'page_obj': page_obj
    }

    if request.headers.get( 'x-requested-with' ) == 'XMLHttpRequest':
        reviews_html = render_to_string( 'main/_parts/feedback_list.jinja', ctx, request = request )
        pagination_html = render_to_string( 'main/_parts/pagination.jinja', ctx, request = request )

        return HttpResponse( reviews_html + pagination_html )

    return render( request, 'main/feedback.jinja', context = ctx )

def licenses(request):
    return render( request, 'main/licenses.jinja' )

def product( request, slug ):
    product = Shaurma.objects.get( slug = slug )
    reviews = Review.objects.filter( shaurma = product.id )
    photos  = ShaurmaImage.objects.filter( shaurma = product.id )

    ctx = {
        'product': product,
        'reviews': reviews,
        'photos' : photos
    }

    return render( request, 'main/product.jinja', context = ctx )

def stock( request, slug ):
    stock = Stock.objects.get( slug = slug )

    ctx = {
        'stock': stock,
    }

    return render( request, 'main/stock.jinja', context = ctx )

def stocks(request):
    stocks = Stock.objects.all()

    ctx = {
        'stocks': stocks
    }    
    return render( request, 'main/stocks.jinja', context = ctx )

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

    return render( request, 'main/search.jinja', context = ctx )

def user(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_owner = request.user.is_authenticated and request.user.username == username
    if not is_owner and not profile_user.is_open:
        return redirect('user_closed')
    return render( request, 'main/user.jinja', {
        'profile_user': profile_user,
        'is_owner': is_owner,
    } )

def user_closed(request):
    return render( request, 'main/_parts/user_closed.jinja' )

def reg(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_django(request, user)
            return redirect('index')
        else:
            print('залупень')
            return render( request, 'main/registration.jinja', { 'form': form } )
    else:
        form = SignUpForm()
        return render( request, 'main/registration.jinja', { 'form': form } )

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
    return render( request, 'main/login.jinja', { 'form': form } )

def logout( request ):
    logout_django(request)
    return redirect('index')

def error_400(request, exception):
    return render( request, 'main/error/400.jinja', status = 400 )

def error_403(request, exception):
    return render( request, 'main/error/403.jinja', status = 403 )

def error_404(request, exception):
    return render( request, 'main/error/404.jinja', status = 404 )

def error_500(request):
    return render( request, 'main/error/500.jinja', status = 500 )
