from django.shortcuts import render

from django.db.models import Count

from main.models import Review, Shaurma, ShaurmaCategory, Stock, ShaurmaImage
from cart.models import Order


def index( request ):
	mode = request.GET.get('mode')  # 'featured' or 'popular'
	try:
		limit = int(request.GET.get('limit', 6))
	except (TypeError, ValueError):
		limit = 6

	stocks = Stock.objects.all()

	if mode == 'featured':
		shaurma = Shaurma.objects.filter(is_featured=True, is_available=True)[:limit]
	else:
		featured = Shaurma.objects.filter(is_featured=True, is_available=True)
		if featured.exists():
			shaurma = featured[:limit]
		else:
			popular_ids = Order.objects.values('shaurma').annotate(cnt=Count('id')).order_by('-cnt').values_list('shaurma', flat=True)[:limit]
			shaurma = Shaurma.objects.filter(id__in=list(popular_ids), is_available=True)

	ctx = {
		'shaurma': shaurma,
		'stocks': stocks
	}
	return render( request, 'main/index.jinja', context = ctx )


def catalog(request):
	shaurma = ShaurmaCategory.objects.all()

	ctx = {
		'shaurma': shaurma
	}
	return render( request, 'main/catalog.jinja', context = ctx )


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
