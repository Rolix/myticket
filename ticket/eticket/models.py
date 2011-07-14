from django.db import models
from django.contrib import admin

class Company(models.Model):
	name = models.CharField("BUS",max_length=50)
	phoneNum = models.IntegerField()
	address = models.CharField(max_length=255)
	email = models.EmailField()
	#booking = models.ForeignKey(Booking)
	def __unicode__(self):
		return self.name

TIME_OF_DAY=(
('Morning','MORNING'),
('Afternoon','AFTERNOON'),
('Night','NIGHT'),
)

NUM_OF_TICKETS=(
 ('1','1 ticket'),
 ('2','2 ticket'),
 ('3','3 ticket'),
 ('4','4'),
 ('5','5'),
)

class Route(models.Model):
	#companyName = models.CharField(max_length=50)
	company = models.ForeignKey(Company)
	departTime = models.CharField("TIME",max_length=40,choices=TIME_OF_DAY )
	origin = models.CharField("FROM",max_length=30)
	destination = models.CharField("TO",max_length=30)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	ticketLeft = models.IntegerField()
	totalTickets = models.IntegerField()
        timeOfDay = models.TimeField()
#        numOfTickets = models.CharField(max_length=1, choices=NUM_OF_TICKETS)
	def __unicode__(self):
		return u'%s-%s, %s, GHS%s'%(self.origin ,self.destination,self.departTime,self.price)

class Booking(models.Model):
	ticketType = models.CharField(max_length=30)
	ticketQuantity = models.IntegerField()
	company = models.ForeignKey(Company)
	route = models.ForeignKey(Route)
	#ticketNum = models.IntegerField()Quajo
	def __unicode__(self):
		return self.ticketType

class Ticket(models.Model):
	ticketNum = models.IntegerField()
	seatNum = models.IntegerField()
	booking = models.ForeignKey(Booking)	

class TicketInline(admin.TabularInline):
	model = Ticket

class BookingAdmin(admin.ModelAdmin):
	inlines=[TicketInline]
MODE_OF_PAYMENT=(
               ('mtn','MTN MONEY'),
               ('airtel','AIRTEL MONEY'),
               ('etranzact','eTRANZACT'),

            )


class Customer(models.Model):
	fName = models.CharField(max_length=20)
	sName = models.CharField(max_length=25)
	phoneNum = models.IntegerField("PHONE NUMBER",help_text='Enter a valid phone number')
	ticketNum = models.ForeignKey(Booking)
        modeOfPayment = models.CharField("MODE OF PAYMENT",max_length=40,choices=MODE_OF_PAYMENT)
	def __unicode__(self):
		pass

class CustomerBookings(models.Model):
       comp = models.CharField(max_length=20)
       cusFrom = models.CharField(max_length=20)
       cusTo = models.CharField(max_length=20)
       cusPhone = models.IntegerField()
       amt = models.DecimalField(max_digits=6, decimal_places=2)
       ticketsbougth = models.IntegerField()
       cusTicketID = models.IntegerField()
       depart = models.TimeField()
       is_cancelled = models.BooleanField(default=False)
       is_valid = models.BooleanField(default=False)
       def __unicode__(self):
           return u'%s-%s, %s, %s, %s'%(self.comp ,self.cusFrom, self.cusTo, self.cusPhone, self.cusTicketID )


class CompanyAdmin(admin.ModelAdmin):
	inlines = [TicketInline]

class Company_admin(models.Model):
	username = models.CharField(max_length=10)
	password = models.CharField(max_length=15)
	fName = models.CharField(max_length=20)
	sName = models.CharField(max_length=25)
	def __unicode__(self):
		pass
admin.site.register(Booking, BookingAdmin)
admin.site.register(Ticket)
admin.site.register(Company)
admin.site.register(Route)
