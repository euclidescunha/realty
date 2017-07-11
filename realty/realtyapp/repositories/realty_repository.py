from realtyapp.daos import AbstractRealtyDao
from realtyapp.domain import RealtyDomain
from realtyapp.exceptions import UnexpectedDAOException


class RealtyRepository:

    def __init__(self, dao):
        if not isinstance(dao, AbstractRealtyDao):
            raise UnexpectedDAOException
        self.dao = dao

    def all(self):
        result = self.dao.all()
        for item in result:
            yield RealtyDomain(**item)

    def filter(self, longitude, latitude, search_nearby):
        result = self.dao.filter(longitude, latitude, search_nearby)
        for item in result:
            yield RealtyDomain(**item)
