from django.conf.urls import patterns, url

from leyning import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^parasha/(?P<parasha_name>[A-Z][a-z]+)/$', views.parasha_detail, name='parasha detail'),
    url(r'^leyner/(?P<leyner_name>[A-Z]\w+)/$', views.leyner_detail, name='leyner detail'),
    url(r'^parasha/snagger/$', views.hebcal_import, name='hebcal import')
)