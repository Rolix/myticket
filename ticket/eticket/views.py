from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from models import Route,Customer,Company,Ticket,CustomerBookings
from django.template import Context, loader
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django import forms
import random
def site_list(request):
	t = loader.get_template('eticket/index.html')
	c = Context(dict())
	return HttpResponse(t.render(c))

class RouteForm(ModelForm):
  	ticketQuantity = forms.IntegerField()
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
      request.session['company'] = request.POST['company']
      request.session['origin'] = request.POST['origin']
      request.session['destination'] = request.POST['destination']
      if form.is_valid():
         r = Route.objects.filter(origin__icontains=request.POST['origin'])\
				.filter(destination__startswith=request.POST['destination'])
         routes = r.filter(company=request.POST['company'])
         if len(routes) == 0:
            return HttpResponse( 'No such Route')
	 request.session['ticketQuantity'] = request.POST['ticketQuantity']
      else:
         return HttpResponse( 'No such Route')
   else:
      return HttpResponse( 'No such Route')
   t = loader.get_template('eticket/book.html')
   c = Context({ 'routes':routes })   
   return HttpResponse(t.render(c)) 



class CustomerForm(ModelForm):
   class Meta:
        exclude = ['ticketNum','fName','sName']
        model = Customer

def purchase_detail(request,id):
     route = Route.objects.get(pk=id)
     if request.method =="POST":
            form = CustomerForm(request.POST) 
            if form.is_valid():
            	form.save()
     else:
            form = CustomerForm()    
     amt_due = float(route.price) * float(request.session['ticketQuantity'])
     request.session['amt_due'] = amt_due
     print request.session['amt_due']
     print request.session['company']
     print request.session['ticketQuantity']
     print request.session['origin']
     print request.session['destination']
     
     t = loader.get_template('eticket/purchase.html')
     c = Context({'form':form.as_p(),'route':route, 'amt_due':amt_due})
     return HttpResponse(t.render(c))

class PayForm(forms.Form):
     pin = forms.CharField( widget=forms.PasswordInput, label="Your PIN" )     
@csrf_exempt
def payment(request):
      #booking = Booking(ticketType='travel',ticketQuantity=request.POST['ticketQuantity'],company=request.POST['company'])
      if request.method == 'POST':
         form = PayForm(request.POST)
         request.session['phoneNum'] = request.POST['phoneNum']
         if form.is_valid():
            form.save()
            return HttpResponseRedirect('')
      else:
            form = CustomerForm() 
      print request.session['phoneNum']   
      t = loader.get_template('eticket/confirmPayment.html')
      c = Context({'form':form.as_p()})
      return HttpResponse(t.render(c)) 
	

@csrf_exempt
def message(request):
        customerbookings = CustomerBookings(comp = request.session['company'], cusFrom = request.session['origin'],cusTo =   request.session['destination'], cusPhone = request.session['phoneNum'],amt = request.session['amt_due'],ticketsbougth = request.session['ticketQuantity'],cusTicketID = random.randrange(10000,20000,2) )
           
        t = loader.get_template('eticket/thank.html')
        c = Context({'customerbookings':customerbookings})
        return HttpResponse(t.render(c))


#def cancel_ticket(request):
	#return


#def event_detail():
	#return
