from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string

from main.models import Location


def locations( request ):
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


def location( request, slug ):
	location_detail = Location.objects.get( slug = slug )

	ctx = {
		'location_detail': location_detail,
	}

	return render( request, 'main/location_detailed.jinja', context = ctx)
