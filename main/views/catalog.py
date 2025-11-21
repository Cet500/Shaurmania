from django.shortcuts import render

from main.models import Review, Shaurma, Stock, ShaurmaImage


def index( request ):
	shaurma = Shaurma.objects.all()
	stocks  = Stock.objects.all()

	ctx = {
		'shaurma': shaurma,
		'stocks': stocks
	}
	return render( request, 'main/index.jinja', context = ctx )


def catalog(request):
	shaurma = Shaurma.objects.all()

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
