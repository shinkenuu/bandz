from rest_framework import serializers
from api_.models import Location, User, Band, Host, Event


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'place_id', 'street', 'number', 'city', 'state', 'country')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'type', 'created', 'location_id')


class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = ('id', 'user_id', 'name', 'genre', 'url', 'fans_amount')


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ('id', 'user_id', 'name', 'url', 'max_capacity', 'location_id')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'location_id', 'starts_at', 'ends_at', 'url', 'host_id')
