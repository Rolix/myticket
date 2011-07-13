from django.conf.urls.defaults import *

urlpatterns = patterns('',
	#url(r'^$', 'eticket.views.home'),
	url(r'^home/?$', 'eticket.views.site_list'),
        url(r'^index/?$', 'eticket.views.site_list'),
	url(r'^route/?$', 'eticket.views.route_detail'),
        url(r'^book/?$', 'eticket.views.book_detail'),
        url(r'^purchase/(?P<id>\d+)/?$','eticket.views.purchase_detail'),
        url(r'^payment/?$', 'eticket.views.payment'),
	url(r'^thank/?$', 'eticket.views.message'),
        url(r'^cancel/?$', 'eticket.views.cancel_ticket'),
        url(r'^confirmCancel/?$', 'eticket.views.confirmCancel'),
)
