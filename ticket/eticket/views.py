from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from models import Route,Customer,Company,Ticket, 
from django.template import Context, loader
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt

def site_list(request):
	t = loader.get_template('eticket/index.html')
	c = Context(dict())
	return HttpResponse(t.render(c))

def booking _details(request):
	return

def route_detail(request):
	return

def purchase_detail(request):
	return 

def cancell_ticket(request):
	return

def events(request):
	return

def event_detail():
	return
