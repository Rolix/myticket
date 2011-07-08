from django.conf.urls.defaults import *

urlpatterns = patterns('',
	#url(r'^$', 'eticket.views.home'),
	url(r'^home/?$', 'eticket.views.site_list'),
	url(r'^route_detail/(\d+)/?$', 'eticket.views.route_detail'),
	url(r'^search/?$', 'eticket.views.search'),
)
