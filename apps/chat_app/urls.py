from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^home$', views.home),
    url(r'^chat$', views.chat),
    url(r'^(?P<id>\d+)/write$', views.write),
    url(r'^(?P<id>\d+)/post$', views.post),
    url(r'^reset$', views.reset)
]