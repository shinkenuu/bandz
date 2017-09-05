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
from django.conf.urls import include, url
from rest_framework.authtoken import views as rest_auth_view
from api_.views import PlaceDetail, PlaceList, MusicGenreDetail, MusicGenreList, UserDetail, UserList, index,\
    FaDetail, FaList, BandDetail, BandList, HostDetail, HostList, EventDetail, EventList,\
    PropositionDetail, PropositionList, EventPublicDetail, EventPublicList

urlpatterns = [
    url(r'^$', index),
    url(r'^auth-token/$', rest_auth_view.obtain_auth_token),
    url(r'^music-genres/', include([
        url(r'^$', MusicGenreList.as_view()),
        url(r'^(?P<pk>\d+)/$', MusicGenreDetail.as_view()),
    ], 'music_genres')),
    url(r'^places/', include([
        url(r'^$', PlaceList.as_view()),
        url(r'^(?P<pk>[a-zA-Z0-9]+)/$', PlaceDetail.as_view()),
    ], 'places')),
    url(r'^users/', include([
        url(r'^$', UserList.as_view()),
        url(r'(?P<pk>\d+)/$', UserDetail.as_view()),
        url(r'(?P<username>[a-zA-Z0-9\-]+)/$', UserDetail.as_view()),
    ], 'users')),
    url(r'^fas/', include([
        url(r'^$', FaList.as_view()),
        url(r'^(?P<pk>\d+)/$', FaDetail.as_view()),
    ], 'fas')),
    url(r'^bands/', include([
        url(r'^$', BandList.as_view()),
        url(r'^(?P<pk>\d+)/$', BandDetail.as_view()),
    ], 'bands')),
    url(r'^hosts/', include([
        url(r'^$', HostList.as_view()),
        url(r'^(?P<pk>\d+)/$', HostDetail.as_view()),
    ], 'hosts')),
    url(r'^events/', include([
        url(r'^$', EventList.as_view()),
        url(r'^(?P<pk>\d+)/$', EventDetail.as_view()),
    ], 'events')),
    url(r'^propositions/', include([
        url(r'^$', PropositionList.as_view()),
        url(r'^(?P<pk>\d+)/$', PropositionDetail.as_view()),
    ], 'propositions')),
    url(r'^event-public/', include([
        url(r'^$', EventPublicList.as_view()),
        url(r'^(?P<pk>\d+)/$', EventPublicDetail.as_view()),
    ], 'event-public')),
]
