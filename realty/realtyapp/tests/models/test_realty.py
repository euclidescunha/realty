import os

from django.conf import settings
from django.test import TestCase

from realtyapp.models import Realty


class RealtyTestCase(TestCase):

    def test_creates_obj_correctly(self):
        obj = Realty(address='TesteAdress', longitude=1, latitude=2)
        obj.save()

        instance = Realty.objects.get(address='TesteAdress')

        self.assertEqual(obj.address, instance.address)
        self.assertEqual(obj.longitude, instance.longitude)
        self.assertEqual(obj.latitude, instance.latitude)
        self.assertEqual((1.0, 2.0), instance.location.coords)
        self.assertFalse(instance.photo)

    def test_creates_obj_with_photo_correctly(self):
        path = os.path.join(settings.BASE_DIR, 'realtyapp', 'tests', 'fixtures', 'photo.png')
        obj = Realty(address='TesteAdress2', photo=path, longitude=1, latitude=2)
        obj.save()

        instance = Realty.objects.get(address='TesteAdress2')

        self.assertEqual(obj.address, instance.address)
        self.assertEqual(obj.longitude, instance.longitude)
        self.assertEqual(obj.latitude, instance.latitude)
        self.assertEqual((1.0, 2.0), instance.location.coords)
        self.assertEqual(path, instance.photo.path)
