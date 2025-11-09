from django.contrib.auth import login as login_django, logout as logout_django, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string

from .factories import (
    ShaurmaFactory,
    ShaurmaCategoryFactory,
    ShaurmaImageFactory,
    LocationFactory,
    UserFactory,
    AchievementFactory,
    UserAchievementFactory,
    ReviewFactory,
    StockFactory,
)
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

def docs( request ):
    return render( request, 'main/docs.jinja' )

def privacy_policy( request ):
    return render( request, 'main/docs/privacy_policy.jinja' )

def user_agreement( request ):
    return render( request, 'main/docs/user_agreement.jinja' )

def user_consent( request ):
    return render( request, 'main/docs/user_consent.jinja' )

def license(request):
    return render( request, 'main/docs/license.jinja' )

def add_license_1( request ):
    return render( request, 'main/docs/add_licence_1.jinja' )

def san_rules(request):
    return render( request, 'main/docs/san_rules.jinja' )

def codex(request):
    return render( request, 'main/docs/codex.jinja' )

def decree(request):
    return render( request, 'main/docs/decree.jinja' )

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

def location_detail( request, slug ):
    location_detail = Location.objects.get( slug = slug )

    ctx = {
        'location_detail': location_detail,
    }

    return render( request, 'main/location_detailed.jinja', context = ctx)

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

@login_required
def dev(request):
    if not request.user.is_superuser:
        return JsonResponse({"detail": "Forbidden"}, status=403 )

    obj = ShaurmaFactory.build()

    data = {k: getattr(obj, k) for k in obj.__dict__ if k not in [ '_state', 'picture', '_ik' ]}

    return JsonResponse( data )


# =====================
# ADMIN: FACTORIES API
# =====================

FACTORY_REGISTRY = {
    'shaurma': ShaurmaFactory,
    'shaurma_category': ShaurmaCategoryFactory,
    'shaurma_image': ShaurmaImageFactory,
    'location': LocationFactory,
    'user': UserFactory,
    'achievement': AchievementFactory,
    'user_achievement': UserAchievementFactory,
    'review': ReviewFactory,
    'stock': StockFactory,
}


def _to_jsonable(value):
    import datetime
    try:
        from django.db.models import Model
    except Exception:
        Model = object  # fallback, should not happen in Django context

    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (datetime.date, datetime.datetime, datetime.time)):
        return value.isoformat()
    if isinstance(value, Model):
        return str(value)
    return str(value)


def _serialize_factory_object(obj):
    exclude_keys = { '_state', '_ik', 'picture', 'image', 'password', '_prefetched_objects_cache' }
    data = {}
    for key, val in obj.__dict__.items():
        if key in exclude_keys:
            continue
        data[key] = _to_jsonable(val)
    return data


@login_required
def admin_factories(request):
    if not request.user.is_superuser:
        return JsonResponse({ 'detail': 'Forbidden' }, status = 403)

    return JsonResponse({
        'available_factories': sorted(list(FACTORY_REGISTRY.keys()))
    })


@login_required
def admin_factory_generate(request, name):
    if not request.user.is_superuser:
        return JsonResponse({ 'detail': 'Forbidden' }, status = 403)

    factory_cls = FACTORY_REGISTRY.get(name)
    if not factory_cls:
        return JsonResponse({ 'detail': 'Factory not found' }, status = 404)

    try:
        count = int(request.GET.get('count', '1'))
    except ValueError:
        count = 1
    count = max(1, min(count, 50))  # simple safety cap

    items = []
    for _ in range(count):
        obj = factory_cls.build()
        items.append(_serialize_factory_object(obj))

    return JsonResponse({ 'factory': name, 'count': len(items), 'items': items })
