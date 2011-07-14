from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from models import Route,Customer,Company,Ticket,CustomerBookings
from django.template import Context, loader
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django import forms
import random, datetime
from django.forms.extras.widgets import SelectDateWidget

def site_list(request):
	t = loader.get_template('eticket/index.html')
	c = Context(dict())
	return HttpResponse(t.render(c))

class RouteForm(ModelForm):
	departDate = forms.DateField(widget = SelectDateWidget(),label = "DATE")
  	ticketQuantity = forms.IntegerField(label ="Number Of Tickets")
	class Meta:
		exclude=['totalTickets','ticketLeft','price','company ','timeOfDay']
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
      request.session['departTime'] = request.POST['departTime']
      if form.is_valid():
         r = Route.objects.filter(origin__icontains=request.POST['origin'])\
				.filter(destination__startswith=request.POST['destination'])
         routes = r.filter(company=request.POST['company'])
	 
         if request.POST['departTime'] == 'Night':
	     start_time = datetime.time(18)
	     end_time = datetime.time(23)
	     routes = routes.filter(timeOfDay__gte=start_time).filter(timeOfDay__lte=end_time)
         elif request.POST['departTime'] == 'Morning':
             start_time = datetime.time(2)
             end_time = datetime.time(12)
             routes = routes.filter(timeOfDay__gte=start_time).filter(timeOfDay__lte=end_time)
         elif request.POST['departTime'] == 'Afternoon':
             start_time = datetime.time(12)
             end_time = datetime.time(16)
             routes = routes.filter(timeOfDay__gte=start_time).filter(timeOfDay__lte=end_time)
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
     #leaves = route.timeOfDay
     request.session['timeOfDay'] = route.timeOfDay
     request.session['company'] = route.company
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
     print request.session['departTime']
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
        customerbookings = CustomerBookings(comp = request.session['company'], cusFrom = request.session['origin'],cusTo =   request.session['destination'], cusPhone = request.session['phoneNum'],amt = request.session['amt_due'],ticketsbougth = request.session['ticketQuantity'],cusTicketID = random.randrange(10000,20000,2),depart=request.session['timeOfDay'] )
        customerbookings.save()   
        t = loader.get_template('eticket/thank.html')
        c = Context({'customerbookings':customerbookings})
        return HttpResponse(t.render(c))


class CancelForm(forms.Form):
     fone = forms.IntegerField(label='Phone Number', help_text="Use puns liberally")
     tickId = forms.IntegerField(label='Ticket Number')

@csrf_exempt
def cancel_ticket(request):
     form = CancelForm()
     t = loader.get_template('eticket/cancel.html')
     c = Context({'form':form.as_p()})
     return HttpResponse(t.render(c))

@csrf_exempt
def confirmCancel(request):
   ticketdet = CustomerBookings.objects.all()
   my = CustomerBookings.objects.all()
   if request.method == 'POST':
      form = CancelForm(request.POST)
      if form.is_valid():
         fone = form.cleaned_data['fone']
         tickId = form.cleaned_data['tickId']
         ticketdet =  ticketdet.filter(cusPhone__iexact=fone).filter(cusTicketID__iexact=tickId) 
         if len(ticketdet) == 0:
              return HttpResponseRedirect(request.path)
         ticketdet.is_cancelled = True
         t = loader.get_template('eticket/confirmCancel.html')
         c = Context({'fone':fone, 'tickId':tickId, 'ticketdet':ticketdet, 'my':my})
         return HttpResponse(t.render(c))
      else:
         return HttpResponse('Invalid form Submision')     
     #ticketdet =  ticketdet.filter(cusPhone__iexact=fone).filter(cusTicketID__iexact=tickId) 
     #if len(ticketdet) == 0:
     # return HttpResponseRedirect(request.path)
   else:
      return HttpResponse('Invalid Submission')
   t = loader.get_template('eticket/confirmCancel.html')
   c = Context({})
   return HttpResponse(t.render(c))


@csrf_exempt
def company_page(request):
	t = loader.get_template('eticket/companyindex.html')
	c = Context(dict())
	return HttpResponse(t.render(c))  

class CustomerBookingsForm(ModelForm):
   class Meta:
        model = CustomerBookings

def bookings(request):
	book_list = CustomerBookings.objects.all()
	t = loader.get_template('eticket/bookings.html')
	c = Context ({'book_list':book_list})
	return HttpResponse(t.render(c))

class ValidationForm(forms.Form):
     fone = forms.IntegerField(label='Phone Number')
     tickId = forms.IntegerField(label='Ticket Number')

@csrf_exempt
def confirmValidation(request):
   ticketdet = CustomerBookings.objects.all()
   my = CustomerBookings.objects.all()
   if request.method == 'POST':
      form = ValidationForm(request.POST)
      if form.is_valid():
         fone = form.cleaned_data['fone']
         tickId = form.cleaned_data['tickId']
         ticketdet =  ticketdet.filter(cusPhone__iexact=fone).filter(cusTicketID__iexact=tickId) 
         if len(ticketdet) == 0:
              return HttpResponseRedirect(request.path)
         ticketdet.is_valid = True
         t = loader.get_template('eticket/confirmValid.html')
         c = Context({'fone':fone, 'tickId':tickId, 'ticketdet':ticketdet, 'my':my})
         return HttpResponse(t.render(c))
      else:
         return HttpResponse('Invalid Booking Form')     
   else:
      return HttpResponse('Invalid Submission')
   t = loader.get_template('eticket/confirmValid.html')
   c = Context({})
   return HttpResponse(t.render(c))

@csrf_exempt
def validate_ticket(request):
     form = CancelForm()
     t = loader.get_template('eticket/valid.html')
     c = Context({'form':form.as_p()})
     return HttpResponse(t.render(c))
