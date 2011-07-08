from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from models import Route,Customer,Company,Ticket
from django.template import Context, loader
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt

def site_list(request):
	t = loader.get_template('eticket/index.html')
	c = Context(dict())
	return HttpResponse(t.render(c))

class RouteForm(ModelForm):
	class Meta:
		exclude=['totalTickets','ticketLeft','price','company ']
		model = Route

def route_detail(request,id):
	route = Route.objects.get(pk=id)
	t = loader.get_template('eticket/route_detail.html')
        c = Context({'route':route})
        return HttpResponse(t.render(c))
	#if request.method="POST":

@csrf_exempt
def search(request):
	form = RouteForm()
	t = loader.get_template('eticket/search.html')
        c = Context({'form':form.as_p()})
        return HttpResponse(t.render(c))
	
		
	
#def booking _details(request):

#def purchase_detail(request):
	#return 

#def cancell_ticket(request):
	#return

#def events(request):
	#return

#def event_detail():
	#return
