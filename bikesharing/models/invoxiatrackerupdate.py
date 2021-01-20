from django.db import models

class InvoxiaTrackerUpdate(models.Model):
    serial      = models.CharField(max_length=50)
    datetime    = models.DateTimeField()
    lat         = models.FloatField()
    lng         = models.FloatField()
    precision   = models.FloatField()
    energy_level= models.FloatField()
    reported = models.DateTimeField(default=None, null=True, blank=True)