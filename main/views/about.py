from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string

from main.models import Review


def about( request ):
	return render( request, 'main/about.jinja' )


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
