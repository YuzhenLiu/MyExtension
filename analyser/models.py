from django.db import models


class CookiesList(models.Model):
    owner = models.CharField(max_length=128)
    cookies = models.JSONField(null=True)


class Cookie(models.Model):
    domain = models.URLField()
    expirationDate = models.CharField(max_length=128, null=True)
    hostOnly = models.BooleanField(null=True)
    httpOnly = models.BooleanField(null=True)
    name = models.CharField(max_length=128, null=True)
    path = models.CharField(max_length=128, null=True)
    sameSite = models.CharField(max_length=128, null=True)
    secure = models.BooleanField(null=True)
    session = models.BooleanField(null=True)
    storeId = models.IntegerField(default=0)
    value = models.CharField(max_length=4096, null=True)