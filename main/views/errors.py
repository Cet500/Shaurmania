from django.shortcuts import render


def error_400(request, exception):
	return render( request, 'main/error/400.jinja', status = 400 )

def error_403(request, exception):
	return render( request, 'main/error/403.jinja', status = 403 )

def error_404(request, exception):
	return render( request, 'main/error/404.jinja', status = 404 )

def error_500(request):
	return render( request, 'main/error/500.jinja', status = 500 )
