from django.conf.urls.defaults import *

urlpatterns = patterns('',
	#url(r'^$', 'eticket.views.home'),
	url(r'^home/?$', 'eticket.views.site_list'),
        url(r'^index/?$', 'eticket.views.site_list'),
	url(r'^route/?$', 'eticket.views.route_detail'),
        url(r'^book/?$', 'eticket.views.book_detail'),
        url(r'^purchase/(?P<id>\d+)/?$','eticket.views.purchase_detail'),
	#url(r'^search/?$', 'eticket.views.search'),
)
