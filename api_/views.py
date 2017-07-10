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
    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAuthenticated, )


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAuthenticated, )


class UserList(generics.ListCreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAuthenticated, )


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAuthenticated, )


class BandList(generics.ListCreateAPIView):
    queryset = models.Band.objects.all()
    serializer_class = serializers.BandSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )


class BandDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Band.objects.all()
    serializer_class = serializers.BandSerializer
    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAuthenticated, )


class HostList(generics.ListCreateAPIView):
    queryset = models.Host.objects.all()
    serializer_class = serializers.HostSerializer
    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAuthenticated, )

class HostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Host.objects.all()
    serializer_class = serializers.HostSerializer
    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAuthenticated, )


class EventList(generics.ListCreateAPIView):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAuthenticated, )


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAuthenticated, )
