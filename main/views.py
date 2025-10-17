from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, Shaurma, Stock, Location, User, Cart
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
    if request.user.is_authenticated:
        # берём корзину из БД
        cart_qs = Cart.objects.filter(user=request.user)
        cart_items = []
        cart_total = 0
        for entry in cart_qs.select_related('item'):
            sh = entry.item
            q = entry.quanity
            item_total = sh.price * q
            cart_items.append({'shaurma': sh, 'quantity': q, 'total': item_total})
            cart_total += item_total
    else:
        # fallback — session (как было)
        cart_data = request.session.get('cart_items', {})
        if isinstance(cart_data, list):
            cart_data = {str(i): 1 for i in cart_data}
            request.session['cart_items'] = cart_data
        cart_items = []
        cart_total = 0
        for id_str, qty in cart_data.items():
            try:
                sh = get_object_or_404(Shaurma, id=int(id_str))
                q = int(qty)
                item_total = sh.price * q
                cart_items.append({'shaurma': sh, 'quantity': q, 'total': item_total})
                cart_total += item_total
            except (ValueError, TypeError):
                continue

    ctx = {'cart': cart_items, 'cart_total': cart_total}
    return render(request, 'main/cart.html', context=ctx)

def cart_add(request, shaurma_id):
    sh = get_object_or_404(Shaurma, id=shaurma_id)
    if request.user.is_authenticated:
        entry, created = Cart.objects.get_or_create(user=request.user, item=sh, defaults={'quanity': 1})
        if not created:
            entry.quanity = entry.quanity + 1
            entry.save(update_fields=['quanity'])
    else:
        cart_data = request.session.get('cart_items', {})
        if isinstance(cart_data, list):
            cart_data = {str(i): 1 for i in cart_data}
        key = str(shaurma_id)
        cart_data[key] = int(cart_data.get(key, 0)) + 1
        request.session['cart_items'] = cart_data
        request.session.modified = True
    return redirect('cart')

def cart_remove(request, shaurma_id):
    sh = get_object_or_404(Shaurma, id=shaurma_id)
    if request.user.is_authenticated:
        try:
            entry = Cart.objects.get(user=request.user, item=sh)
            if entry.quanity > 1:
                entry.quanity -= 1
                entry.save(update_fields=['quanity'])
            else:
                entry.delete()
        except Cart.DoesNotExist:
            pass
    else:
        cart_data = request.session.get('cart_items', {})
        if isinstance(cart_data, list):
            cart_data = {str(i): 1 for i in cart_data}
        key = str(shaurma_id)
        if key in cart_data:
            new_qty = int(cart_data.get(key, 0)) - 1
            if new_qty > 0:
                cart_data[key] = new_qty
            else:
                del cart_data[key]
            request.session['cart_items'] = cart_data
            request.session.modified = True
    return redirect('cart')

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

def product( request, slug ):
    product = Shaurma.objects.get( slug = slug )
    reviews = Review.objects.filter( shaurma = product.id )

    ctx = {
        'product': product,
        'reviews': reviews
    }

    return render( request, 'main/product.html', context = ctx )

def stock( request, slug ):
    stock = Stock.objects.get( slug = slug )

    ctx = {
        'stock': stock,
    }

    return render( request, 'main/stock.html', context = ctx )

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
