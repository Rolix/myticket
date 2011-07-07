from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$', 'eticket.views.home'),
	url(r'^home/?$', 'eticket.views.site_list'),
)
