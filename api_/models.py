from datetime import datetime
from django.db import models

USER_TYPES = (
    (1, u'fa'),
    (2, u'band'),
    (3, u'recorder'),
    (4, u'venue'))


class Location(models.Model):
    place_id = models.CharField(unique=True, max_length=255, default='', db_index=True)
    street = models.CharField(max_length=100, null=True)
    number = models.IntegerField()
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=30, null=True)


class User(models.Model):
    first_name = models.CharField(null=False, default='', max_length=30)
    last_name = models.CharField(null=False, default='', max_length=50)
    email = models.EmailField(null=False, default='', unique=True, db_index=True)
    type = models.IntegerField(choices=USER_TYPES)
    created = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location, default=-1)


class Band(models.Model):
    user_id = models.ForeignKey(User, null=True)
    name = models.CharField(null=False, default='', max_length=80)
    genre = models.CharField(max_length=20)
    url = models.URLField()
    fans_amount = models.BigIntegerField()


class Host(models.Model):
    user_id = models.ForeignKey(User, null=True)
    name = models.CharField(null=False, default='', max_length=80)
    url = models.URLField()
    max_capacity = models.BigIntegerField()
    location = models.ForeignKey(Location, default=-1)


class Event(models.Model):
    name = models.CharField(null=False, default='', max_length=80)
    location = models.ForeignKey(Location, default=-1)
    starts_at = models.DateTimeField(null=False, default=datetime.min)
    ends_at = models.DateTimeField(null=False, default=datetime.max)
    url = models.URLField()
    # presenting
    host = models.ForeignKey(Host, default=-1)
