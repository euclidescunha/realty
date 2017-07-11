from realtyapp.daos import AbstractRealtyDao
from realtyapp.exceptions import UnexpectedDAOException
from realtyapp.services import GoogleGeoCoder


class CreateRealtyUseCase:

    def __init__(self, dao):
        if not isinstance(dao, AbstractRealtyDao):
            raise UnexpectedDAOException

        self.dao = dao
        self.geocoder = GoogleGeoCoder()

    def execute(self, address, photo):
        latitude, longitude = self.geocoder.coordinates_from(address)
        self.dao.create(address, photo, longitude, latitude)
