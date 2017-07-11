from realtyapp.repositories import RealtyRepository
from realtyapp.services import GoogleGeoCoder


class ListRealtyByAddressUseCase:
    def __init__(self, dao):
        self.repository = RealtyRepository(dao)
        self.geocoder = GoogleGeoCoder()

    def execute(self, address=None, search_nearby=False):
        if address:
            latitude, longitude = self.geocoder.coordinates_from(address)
            return self.repository.filter(
                longitude=longitude,
                latitude=latitude,
                search_nearby=search_nearby
            )
        return self.repository.all()
