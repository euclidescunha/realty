from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from core.daos import AbstractRealtyDao
from core.models import Realty


class RealtyMapper:

    @classmethod
    def map(cls, obj):
        return {
            'address': obj.address,
            'photo': obj.photo,
            'longitude': obj.longitude,
            'latitude': obj.latitude,
            'location': obj.location,
        }


class RealtyDAO(AbstractRealtyDao):

    mapper = RealtyMapper

    def create(self, address, photo, longitude, latitude):
        Realty.objects.create(
            address=address,
            photo=photo,
            longitude=longitude,
            latitude=latitude,
        )

    def all(self):
        result = Realty.objects.all().order_by('-id')
        for item in result:
            yield self.mapper.map(item)

    def filter(self, longitude, latitude, search_nearby):
        point = Point(longitude, latitude)

        if search_nearby:
            result = Realty.objects.filter(
                location__distance_lte=(point, D(km=30))
            )
        else:
            result = Realty.objects.filter(
                location__distance_lte=(point, D(km=1))
            )

        result = result.distance(point).order_by('distance')

        for item in result:
            yield self.mapper.map(item)
