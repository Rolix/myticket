from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from models import Route,Customer,Company,Ticket
from django.template import Context, loader
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

def site_list(request):
	t = loader.get_template('eticket/index.html')
	c = Context(dict())
	return HttpResponse(t.render(c))

class RouteForm(ModelForm):
	class Meta:
		exclude=['totalTickets','ticketLeft','price','company ']
		model = Route

def route_detail(request):
        if request.method =="POST":
            form = RouteForm(request.POST)
            if form.is_valid():
               form.save()
               return HttpResponseRedirect('')
        else:
            form = RouteForm()    
	t = loader.get_template('eticket/route.html')
        c = Context({'form':form.as_p()})
        return HttpResponse(t.render(c))
	
@csrf_exempt			
def book_detail(request):
   if request.method == 'POST':
      form = RouteForm(request.POST)
      if form.is_valid():
           r = Route.objects.filter(origin__icontains=request.POST['origin'])
           r = r.filter(destination__icontains=request.POST['destination'])
           routes = r.filter(company=request.POST['company'])
           if len(routes) == 0:
             return HttpResponse( 'No such Route')
#           print 'Company', route.company
#           print 'Tickets left', route.ticketLeft
#           assert False
   t = loader.get_template('eticket/book.html')
   c = Context({ 'routes':routes })   
   return HttpResponse(t.render(c)) 



class CustomerForm(ModelForm):
   class Meta:
        exclude = ['ticketNum','fName','sName']
        model = Customer

def purchase_detail(request,id):
     if request.method =="POST":
            form = CustomerForm(request.POST)
            if form.is_valid():
               form.save()
     else:
            form = CustomerForm()    
     t = loader.get_template('eticket/purchase.html')
     c = Context({'form':form.as_p()})
     return HttpResponse(t.render(c))
     
	

#@csrf_exempt
#def search(request):
#	form = RouteForm()
#	t = loader.get_template('eticket/search.html')
 #       c = Context({'form':form.as_p()})
  #      return HttpResponse(t.render(c))


#def cancel_ticket(request):
	#return

#def events(request):
	#return

#def event_detail():
	#return
