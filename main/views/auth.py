from django.contrib.auth import login as login_django, logout as logout_django, authenticate
from django.shortcuts import render, redirect
from main.forms import SignUpForm, LoginForm


def reg(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login_django(request, user)
			return redirect('index')
		else:
			print('залупень')
			return render( request, 'main/registration.jinja', { 'form': form } )
	else:
		form = SignUpForm()
		return render( request, 'main/registration.jinja', { 'form': form } )


def login(request):
	form = LoginForm(data=request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login_django(request, user)
				return redirect('index')
	return render( request, 'main/login.jinja', { 'form': form } )


def logout( request ):
	logout_django(request)
	return redirect('index')
