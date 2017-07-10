class AbstractRealtyDao:

    def create(self, address, image, longitude, latitude):
        raise NotImplementedError

    def all(self):
        raise NotImplementedError

    def filter(self, longitude, latitude, search_nearby):
        raise NotImplementedError
