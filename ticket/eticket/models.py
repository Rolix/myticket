from django.db import models

class Booking(models.Model):
	ticketType = models.CharField(max_length=30)
	ticketQuantity = models.IntegerField()
	ticketNum = models.IntegerField()
	seatNum = models.IntegerField()
	def __unicode__(self):
		pass

class Customer(models.Model):
	fName = models.CharField(max_length=20)
	sName = models.CharField(max_length=25)
	phoneNum = models.IntegerField()
	ticketNum = models.ForeignKey(Booking)
	def __unicode__(self):
		pass

class Company(models.Model):
	name = models.CharField(max_length=50)
	phoneNum = models.IntegerField()
	address = models.CharField(max_length=255)
	email = models.EmailField()
	ticketNum = models.ForeignKey(Booking)
 	def __unicode__(self):
		return self.name

class Route(models.Model):
	companyName = models.CharField(max_length=50)
	departTime = models.DateTimeField()
	origin = models.CharField(max_length=30)
	destination = models.Charfield(max_length=30)
	price = models.DecimalField(max_digits=4, decimal_places=2)
	ticketLeft = models.IntegerField()
	totalTickets = models.IntegerField()
	ticketNum = models.ForeignKey(Booking)
	def __unicode__(self):
		pass

class CompanyAdmin(models.Model):
	username = models.CharField(max_length=10)
	password = models.CharField(max_length=15)
	fName = models.CharField(max_length=20)
	sName = models.CharField(max_length=25)
	def __unicode__(self):
		pass
