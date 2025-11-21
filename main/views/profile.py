from django.shortcuts import render, redirect, get_object_or_404
from main.models import User


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
