from django.http import HttpResponse
from rest_framework import authentication, generics, permissions
from api_ import models
from bandz import serializers


def index(request):
    """
    
    :param request: 
    :return: 
    """
    return HttpResponse(content='Yeah, Im alive')


class LocationList(generics.ListCreateAPIView):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer


class UserList(generics.ListCreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class BandList(generics.ListCreateAPIView):
    queryset = models.Band.objects.all()
    serializer_class = serializers.BandSerializer


class BandDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Band.objects.all()
    serializer_class = serializers.BandSerializer


class HostList(generics.ListCreateAPIView):
    queryset = models.Host.objects.all()
    serializer_class = serializers.HostSerializer


class HostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Host.objects.all()
    serializer_class = serializers.HostSerializer


class EventList(generics.ListCreateAPIView):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
