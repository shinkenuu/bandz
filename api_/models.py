from django.contrib.auth.models import User
from django.db.models import Model, CharField, TextField, DecimalField, DateTimeField, DateField, BigIntegerField,\
    PositiveSmallIntegerField, BooleanField, NullBooleanField, URLField, ForeignKey, OneToOneField, ManyToManyField
from django.utils import timezone

EVENT_RATING_CHOICES = (
    (1, 'bad'),
    (2, 'meh'),
    (3, 'nice'),
    (4, 'awesome'),
    (5, 'loved it'),
)

FAN_AT_EVENT_FEELING_CHOICES = (
    (u'i', 'interested'),
    (u'n', 'nah'),
    (u'g', 'going'),
)


class Place(Model):
    id = CharField(unique=True, max_length=255, primary_key=True)
    formatted_address = CharField(max_length=255, null=True)
    latitude = DecimalField(decimal_places=6, max_digits=9, null=True)
    longitude = DecimalField(decimal_places=6, max_digits=9, null=True)

    def __str__(self):
        return self.formatted_address


class MusicGenre(Model):
    name = CharField(unique=True, max_length=30)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Music Genres'

    def __str__(self):
        return self.name


class UserProfile(Model):
    user = OneToOneField(User)
    firebase_uid = CharField(max_length=255, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.EMAIL_FIELD


class Fa(UserProfile):
    birth_date = DateField(default=timezone.now)
    place = ForeignKey(Place)
    music_genres = ManyToManyField('MusicGenre')
    events = ManyToManyField('Event', through='EventPublic', through_fields=('fa', 'event'))

    def __str__(self):
        return self.user.get_full_name()


class Band(UserProfile):
    name = CharField(max_length=80)
    description = TextField()
    url = URLField()
    place = ForeignKey(Place)
    music_genres = ManyToManyField('MusicGenre')

    def __str__(self):
        return self.name


class Host(UserProfile):
    name = CharField(max_length=80)
    description = TextField()
    url = URLField()
    max_capacity = BigIntegerField()
    place = ForeignKey(Place)
    music_genres = ManyToManyField('MusicGenre')

    def __str__(self):
        return self.name


class Event(Model):
    name = CharField(max_length=80)
    description = TextField()
    url = URLField(null=True)
    starts_at = DateTimeField()
    ends_at = DateTimeField()
    min_age = PositiveSmallIntegerField()
    music_genres = ManyToManyField('MusicGenre')
    price = DecimalField(max_digits=6, decimal_places=2)
    host = ForeignKey(Host, related_name='events')
    band = ForeignKey(Band, related_name='events', null=True)
    confirmed = BooleanField(default=False)
    public = ManyToManyField('Fa', through='EventPublic', through_fields=('event', 'fa'))

    class Meta:
        unique_together = (('name', 'host', 'starts_at'), )

    def __str__(self):
        return self.name


class Proposition(Model):
    band = ForeignKey(Band, related_name='propositions')
    host = ForeignKey(Host, related_name='propositions')
    event = ForeignKey(Event, related_name='propositions')
    message = TextField(null=False)
    price = DecimalField(max_digits=6, decimal_places=2)
    confirmed = NullBooleanField(default=None)

    class Meta:
        unique_together = (('band', 'event'), )

    def __str__(self):
        return '{}\'s to play at {}'.format(self.band.name, self.event.name)


class EventPublic(Model):
    fa = ForeignKey(Fa)
    event = ForeignKey(Event)
    feeling = CharField(null=True, choices=FAN_AT_EVENT_FEELING_CHOICES, max_length=1)
    rating = PositiveSmallIntegerField(null=True, choices=EVENT_RATING_CHOICES)
    comment = TextField(null=True)

    class Meta:
        verbose_name_plural = "Event's Public"
        unique_together = (('fa', 'event'), )

    def __str__(self):
        return '{} about {}'.format(self.fa.user.get_full_name(), self.event.name)
