from django.db import models

class InvoxiaTrackerUpdate(models.Model):
    serial      = models.CharField(max_length=50)
    datetime    = models.DateTimeField(default=None, null=True, blank=True)
    lat         = models.FloatField()
    lng         = models.FloatField()
    precision   = models.FloatField(default=None, null=True, blank=True)
    energy_level= models.FloatField(default=None, null=True, blank=True)
    reported = models.DateTimeField(default=None, null=True, blank=True)