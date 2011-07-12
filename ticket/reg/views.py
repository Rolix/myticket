from django.template import Context, loader
from django.http import HttpResponse
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

@csrf_exempt
def loginView(request):
	if request.method == 'POST':
		uname = request.POST['username']
		passwd= request.POST['password']
		user = authenticate(username=uname,password=passwd)
		if user is not None:
			if user.is_active:
				login(request,user)
				t = loader.get_template('eticket/base.html')
				c = Context(dict())
				return HttpResponse(t.render(c))
		else:
			return render_to_response('reg/incorrect.html')
	form = LoginForm()
	return render_to_response('reg/login.html', {'form': form,'logged_in': request.user.is_authenticated()})


@csrf_exempt
def logoutView(request):
	logout(request)
	return render_to_response('reg/logout.html')

def incorrectView(request):

	return render_to_response('reg/incorrect.html')
