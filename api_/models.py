from django.contrib.auth.models import User
from django.db import models

USER_TYPES_CHOICES = (
    (u'f', u'fa'),
    (u'b', u'band'),
    (u'h', u'host'),
)

EVENT_RATING_CHOICES = (
    (1, 'bad'),
    (2, 'meh'),
    (3, 'nice'),
    (4, 'awesome'),
    (5, 'loved it'),
)

FAN_AT_EVENT_FEELING_CHOICES = (
    (u'm', 'maybe'),
    (u'i', 'interested'),
    (u'n', 'nah'),
    (u'g', 'going'),
)


class Location(models.Model):
    place_id = models.CharField(unique=True, max_length=255, db_index=True)
    street = models.CharField(max_length=100, null=True)
    number = models.IntegerField()
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=2, null=True)
    country = models.CharField(max_length=30, null=True)

    def __str__(self):
        return '{}, n{} - {} - {} - {}'.format(
            self.street, self.number, self.city, self.state, self.country)


class MusicGenre(models.Model):
    name = models.CharField(unique=True, max_length=30)
    parent_genre = models.ForeignKey('MusicGenre', null=True)

    def __str__(self):
        return '{} music genre'.format(self.name)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    type = models.CharField(choices=USER_TYPES_CHOICES, max_length=1, default='f')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.EMAIL_FIELD


class Fa(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    location = models.ForeignKey(Location)
    favorite_genres = models.ManyToManyField('MusicGenre', through='FaMusicTaste', through_fields=('fa', 'music_genre'))
    events = models.ManyToManyField('Event', through='FaAtEvent', through_fields=('fa', 'event'))

    def __str__(self):
        return 'Fa {} {}'.format(self.first_name, self.last_name)


class Band(models.Model):
    user_profile = models.ForeignKey(UserProfile, null=True)
    name = models.CharField(max_length=80)
    description = models.TextField()
    genre = models.ManyToManyField('MusicGenre', through='BandGenre', through_fields=('band', 'music_genre'))
    url = models.URLField()
    fans_amount = models.BigIntegerField(default=0)
    location = models.ForeignKey(Location)
    events = models.ManyToManyField('Event', through='BandAtEvent', through_fields=('band', 'event'))

    def __str__(self):
        return 'Band {}'.format(self.name)


class Host(models.Model):
    user_profile = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=80)
    description = models.TextField(null=True)
    url = models.URLField()
    max_capacity = models.BigIntegerField()
    location = models.ForeignKey(Location)
    events = models.ManyToManyField('Event', through='EventAtHost', through_fields=('host', 'event'))

    def __str__(self):
        return 'Host {}'.format(self.name)


class Event(models.Model):
    name = models.CharField(max_length=80)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    min_age = models.PositiveSmallIntegerField()
    url = models.URLField()
    presenting_bands = models.ManyToManyField('Band', through='BandAtEvent', through_fields=('event', 'band'))
    hosts = models.ManyToManyField('Host', through='EventAtHost', through_fields=('event', 'host'))

    def __str__(self):
        return 'Event '.format(self.name)


class Proposition(models.Model):
    band = models.ForeignKey(Band)
    host = models.ForeignKey(Host)
    message = models.TextField(null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    closed = models.BooleanField(default=False)

    def __str__(self):
        return 'Prop between band {} and host {}'.format(self.band.name, self.host.name)


class EventAtHost(models.Model):
    event = models.ForeignKey(Event)
    host = models.ForeignKey(Host)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return 'Event {} at host {}'.format(self.event.name, self.host.name)


class BandAtEvent(models.Model):
    band = models.ForeignKey(Band)
    event = models.ForeignKey(Event)
    starts_at = models.DateTimeField(null=False)
    ends_at = models.DateTimeField(null=False)

    def __str__(self):
        return 'Band {} at event {}'.format(self.band.name, self.event.name)


class FaAtEvent(models.Model):
    fa = models.ForeignKey(Fa)
    event = models.ForeignKey(Event)
    feeling = models.CharField(null=True, choices=FAN_AT_EVENT_FEELING_CHOICES, max_length=1)
    rating = models.PositiveSmallIntegerField(null=True, choices=EVENT_RATING_CHOICES)

    def __str__(self):
        return 'Fa {} about event {}'.format(self.fa.first_name, self.event.name)


class Fa2Band(models.Model):
    band = models.ForeignKey(Band)
    fa = models.ForeignKey(Fa)
    subscribed = models.BooleanField(default=False)

    def __str__(self):
        return 'Fa {} about Band {}'.format(self.fa.first_name, self.band.name)


class FaMusicTaste(models.Model):
    fa = models.ForeignKey(Fa)
    music_genre = models.ForeignKey(MusicGenre)

    def __str__(self):
        return 'Fa {} likes {} music'.format(self.fa.first_name, self.music_genre.name)


class BandGenre(models.Model):
    band = models.ForeignKey(Band)
    music_genre = models.ForeignKey(MusicGenre)
    degree = models.PositiveSmallIntegerField()

    def __str__(self):
        return 'Band {} plays {} music'.format(self.band.name, self.music_genre.name)
