from datetime import datetime
from django.db import models

USER_TYPES = (
    (u'f', u'fa'),
    (u'b', u'band'),
    (u'r', u'recorder'),
    (u'h', u'host'))


class Location(models.Model):
    place_id = models.CharField(unique=True, max_length=255, db_index=True)
    street = models.CharField(max_length=100, null=True)
    number = models.IntegerField()
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=30, null=True)


class User(models.Model):
    first_name = models.CharField(null=False, max_length=30)
    last_name = models.CharField(null=False, max_length=50)
    email = models.EmailField(null=False, unique=True, db_index=True)
    type = models.CharField(max_length=10, choices=USER_TYPES)
    created = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location)


class Band(models.Model):
    user_id = models.ForeignKey(User, null=True)
    name = models.CharField(null=False, max_length=80)
    genre = models.CharField(max_length=20)
    url = models.URLField()
    fans_amount = models.BigIntegerField()


class Host(models.Model):
    user_id = models.ForeignKey(User, null=True)
    name = models.CharField(null=False, max_length=80)
    url = models.URLField()
    max_capacity = models.BigIntegerField()
    location = models.ForeignKey(Location)


class Event(models.Model):
    name = models.CharField(null=False, max_length=80)
    location = models.ForeignKey(Location)
    starts_at = models.DateTimeField(null=False)
    ends_at = models.DateTimeField(null=False)
    url = models.URLField()
    # presenting
    host = models.ForeignKey(Host)
