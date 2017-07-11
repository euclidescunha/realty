import os
from unittest.mock import call, Mock, patch

from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.test import TestCase

from realtyapp.daos import RealtyDAO
from realtyapp.models import Realty


class RealtyDAOTestCase(TestCase):

    def setUp(self):
        patcher = patch('core.daos.real_estate_dao.Realty', spec=True)
        self.orm = patcher.start()

        self.dao = RealtyDAO()

        self.addCleanup(patcher.stop)

    def test_create_calls_orm_correctly(self):
        self.dao.create('address', 'photo', 'longitude', 'latitude')

        self.orm.objects.create.assert_called_once_with(
            address='address',
            photo='photo',
            longitude='longitude',
            latitude='latitude',
        )

    def test_all_calls_orm_correctly(self):
        expected = [{'id': 1}, {'id': 2}]
        self.dao.mapper = Mock(self.dao.mapper)

        self.dao.mapper.map.side_effect = expected
        self.orm.objects.all().order_by.return_value = [1, 2]

        result = list(self.dao.all())

        self.orm.objects.all().order_by.assert_called_once_with('-id')
        self.assertEqual(2, self.dao.mapper.map.call_count)
        self.dao.mapper.map.assert_has_calls([call(1), call(2)])
        self.assertEqual(expected, result)

    def test_filter_calls_orm_correctly(self):
        expected = [{'id': 1}, {'id': 2}]
        expected_point = Point(1, 2)
        self.dao.mapper = Mock(self.dao.mapper)

        self.dao.mapper.map.side_effect = expected
        self.orm.objects.filter().distance().order_by.return_value = [1, 2]

        result = list(self.dao.filter(1, 2, False))

        self.orm.objects.filter.assert_called_with(
            location__distance_lte=(expected_point, D(km=1))
        )
        self.orm.objects.filter().distance.assert_called_with(expected_point)
        self.orm.objects.filter().distance().order_by.assert_called_once_with('distance')
        self.assertEqual(2, self.dao.mapper.map.call_count)
        self.dao.mapper.map.assert_has_calls([call(1), call(2)])
        self.assertEqual(expected, result)

    def test_filter_with_search_nearby_calls_orm_correctly(self):
        expected = [{'id': 1}, {'id': 2}]
        expected_point = Point(1, 2)
        self.dao.mapper = Mock(self.dao.mapper)

        self.dao.mapper.map.side_effect = expected
        self.orm.objects.filter().distance().order_by.return_value = [1, 2]

        result = list(self.dao.filter(1, 2, True))

        self.orm.objects.filter.assert_called_with(
            location__distance_lte=(expected_point, D(km=30))
        )
        self.orm.objects.filter().distance.assert_called_with(expected_point)
        self.orm.objects.filter().distance().order_by.assert_called_once_with('distance')
        self.assertEqual(2, self.dao.mapper.map.call_count)
        self.dao.mapper.map.assert_has_calls([call(1), call(2)])
        self.assertEqual(expected, result)


class RealtyMapperTestCase(TestCase):

    def setUp(self):
        path = os.path.join(settings.BASE_DIR, 'core', 'tests', 'fixtures', 'photo.png')
        self.obj = Realty(
            address='Adress',
            photo=path,
            longitude=1,
            latitude=2,
        )
        self.obj.save()

        self.dao = RealtyDAO()

    def test_map_obj_correctly(self):
        expected = {
            'address': self.obj.address,
            'photo': self.obj.photo,
            'longitude': self.obj.longitude,
            'latitude': self.obj.latitude,
            'location': self.obj.location,
        }

        data = self.dao.mapper.map(self.obj)
        self.assertEqual(expected, data)
