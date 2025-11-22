from django.shortcuts import render
from main.models import Stock


def stocks(request):
	stocks = Stock.objects.all()

	ctx = {
		'stocks': stocks
	}

	return render( request, 'main/stocks.jinja', context = ctx )


def stock( request, slug ):
	stock = Stock.objects.get( slug = slug )

	ctx = {
		'stock': stock,
	}

	return render( request, 'main/stock.jinja', context = ctx )

