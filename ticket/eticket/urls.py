from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$', 'eticket.views.home'),
)
