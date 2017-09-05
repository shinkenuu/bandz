from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.status import HTTP_200_OK
from rest_framework.generics import ListAPIView, RetrieveAPIView, \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from .models import Place, MusicGenre, User, Fa, Band, Host, Event, Proposition, EventPublic
from bandz.serializers import PlaceSerializer, MusicGenreSerializer, UserSerializer, FaSerializer, BandSerializer, \
    HostSerializer, EventSerializer, NewPropositionSerializer, ExistingPropositionSerializer, EventPublicSerializer


def index(request):
    """
    
    :param request: 
    :return: 
    """
    return render(request, template_name='api/index.html', context={})


class PlaceList(ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class PlaceDetail(RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class MusicGenreList(ListAPIView):
    queryset = MusicGenre.objects.all()
    serializer_class = MusicGenreSerializer


class MusicGenreDetail(RetrieveAPIView):
    queryset = MusicGenre.objects.all()
    serializer_class = MusicGenreSerializer


class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FaList(ListCreateAPIView):
    queryset = Fa.objects.all()
    serializer_class = FaSerializer


class FaDetail(RetrieveUpdateDestroyAPIView):
    queryset = Fa.objects.all()
    serializer_class = FaSerializer


class BandList(ListCreateAPIView):
    queryset = Band.objects.all()
    serializer_class = BandSerializer


class BandDetail(RetrieveUpdateDestroyAPIView):
    queryset = Band.objects.all()
    serializer_class = BandSerializer


class HostList(ListCreateAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class HostDetail(RetrieveUpdateDestroyAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class EventList(ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetail(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class PropositionList(ListCreateAPIView):
    queryset = Proposition.objects.all()
    serializer_class = NewPropositionSerializer


class PropositionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Proposition.objects.all()
    serializer_class = ExistingPropositionSerializer

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        if response.status_code == HTTP_200_OK and response.data.get('confirmed', False):
            instance = self.get_object()
            event_filter = {
                'pk': instance.event_id
            }
            event = get_object_or_404(Event.objects.all(), **event_filter)
            event.band = instance.band
            event.confirmed = True
            event.save()
        return response


class EventPublicList(ListCreateAPIView):
    queryset = EventPublic.objects.all()
    serializer_class = EventPublicSerializer


class EventPublicDetail(RetrieveUpdateDestroyAPIView):
    queryset = EventPublic.objects.all()
    serializer_class = EventPublicSerializer
