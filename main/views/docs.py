from django.shortcuts import render


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
