from django.conf.urls.defaults import *
urlpatterns = patterns('',	
	url(r'^login/$', 'reg.views.loginView'),
	url(r'^logout/$', 'reg.views.logoutView'),
	url(r'^incorrect/$', 'reg.views.incorrectView'),
)

