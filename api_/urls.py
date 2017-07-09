"""api_ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from rest_framework.authtoken import views as rest_auth_view
from api_ import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^auth-token/$', rest_auth_view.obtain_auth_token),
    url(r'^locations/$', views.LocationList.as_view()),
    url(r'^locations/(?P<pk>[0-9]+)/$', views.LocationDetail.as_view()),
    url(r'^locations/(?P<placeid>[a-zA-Z0-9]+)/$', views.LocationDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^bands/$', views.BandList.as_view()),
    url(r'^bands/(?P<pk>[0-9]+)/$', views.BandDetail.as_view()),
    url(r'^bands/(?P<name>[a-zA-Z0-9]+)/$', views.BandDetail.as_view()),
    url(r'^hosts/$', views.HostList.as_view()),
    url(r'^hosts/(?P<pk>[0-9]+)/$', views.HostDetail.as_view()),
    url(r'^hosts/(?P<location_id>[0-9]+)/$', views.HostDetail.as_view()),
    url(r'^hosts/(?P<name>[a-zA-Z0-9]+)/$', views.HostDetail.as_view()),
    url(r'^events/$', views.EventList.as_view()),
    url(r'^events/(?P<pk>[0-9]+)/$', views.EventDetail.as_view()),
    url(r'^events/(?P<location_id>[0-9]+)/$', views.EventDetail.as_view()),
]
