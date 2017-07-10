from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class Realty(models.Model):
    address = models.CharField(max_length=200)
    photo = models.ImageField(null=True, blank=True)
    location = models.PointField(geography=True, srid=4326)
    longitude = models.FloatField()
    latitude = models.FloatField()

    objects = models.GeoManager()

    def save(self, **kwargs):
        self.location = Point(self.longitude, self.latitude)
        super(Realty, self).save(**kwargs)
