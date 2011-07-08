from django.db import models
from django.contrib import admin

class Company(models.Model):
	name = models.CharField(max_length=50)
	phoneNum = models.IntegerField()
	address = models.CharField(max_length=255)
	email = models.EmailField()
	#booking = models.ForeignKey(Booking)
	def __unicode__(self):
		return self.name

class Route(models.Model):
	#companyName = models.CharField(max_length=50)
	company = models.ForeignKey(Company)
	departTime = models.DateTimeField()
	origin = models.CharField(max_length=30)
	destination = models.CharField(max_length=30)
	price = models.DecimalField(max_digits=4, decimal_places=2)
	ticketLeft = models.IntegerField()
	totalTickets = models.IntegerField()
	def __unicode__(self):
		return u'%s-%s, %s, GHS%s'%(self.origin ,self.destination,self.departTime,self.price)

class Booking(models.Model):
	ticketType = models.CharField(max_length=30)
	ticketQuantity = models.IntegerField()
	company = models.ForeignKey(Company)
	route = models.ForeignKey(Route)
	#ticketNum = models.IntegerField()
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

class Customer(models.Model):
	fName = models.CharField(max_length=20)
	sName = models.CharField(max_length=25)
	phoneNum = models.IntegerField()
	ticketNum = models.ForeignKey(Booking)
	def __unicode__(self):
		pass


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
