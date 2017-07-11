from geopy.geocoders import GoogleV3 as Google

from django.conf import settings

class GoogleGeoCoder:

    def __init__(self):
        self.geocoder = Google(settings.GOOGLE_API_KEY)

    def search(self, address, search_exactly):
        return self.geocoder.geocode(
            query=address,
            exactly_one=search_exactly,
        )

    def coordinates_from(self, address):
        _, coordinates = self.search(address, True)
        return coordinates
