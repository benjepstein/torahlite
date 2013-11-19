from django.conf.urls import patterns, include, url
from django.contrib import admin
from leyning import views
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.redirect_index),
	(r'^admin/',include(admin.site.urls)),
	(r'^leyning/', include('leyning.urls', namespace='leyning')),

    # Examples:
    # url(r'^$', 'torahlite.views.home', name='home'),
    # url(r'^torahlite/', include('torahlite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
