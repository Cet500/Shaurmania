from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string

from main.models import News, NewsTag


def news( request, tag_slug=None ):
	news_list   = News.objects.filter(is_shown=True).order_by('-created_at')
	all_tags    = NewsTag.objects.all()
	current_tag = None

	if tag_slug:
		current_tag = get_object_or_404( NewsTag, slug = tag_slug )
		news_list = news_list.filter( tags__slug = current_tag.slug )

	paginator = Paginator( news_list, 20 )

	page_number = request.GET.get('page')
	page_obj = paginator.get_page( page_number )

	ctx = {
		'all_tags'   : all_tags,
		'current_tag': current_tag,
		'page_obj'   : page_obj
	}

	if request.headers.get( 'x-requested-with' ) == 'XMLHttpRequest':
		reviews_html = render_to_string( 'main/_parts/news_list.jinja', ctx, request = request )
		pagination_html = render_to_string( 'main/_parts/pagination.jinja', ctx, request = request )

		return HttpResponse( reviews_html + pagination_html )

	return render( request, 'main/news.jinja', context = ctx )


def news_detail( request, slug ):
	return render( request, 'main/news_detailed.jinja' )
