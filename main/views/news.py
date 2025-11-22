from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string

from main.models import News


def news( request ):
	news = News.objects.filter(is_shown=True).order_by('-created_at')
	paginator = Paginator( news, 20 )

	page_number = request.GET.get('page')
	page_obj = paginator.get_page( page_number )

	ctx = {
		'page_obj': page_obj
	}

	if request.headers.get( 'x-requested-with' ) == 'XMLHttpRequest':
		reviews_html = render_to_string( 'main/_parts/news_list.jinja', ctx, request = request )
		pagination_html = render_to_string( 'main/_parts/pagination.jinja', ctx, request = request )

		return HttpResponse( reviews_html + pagination_html )

	return render( request, 'main/news.jinja', context = ctx )
