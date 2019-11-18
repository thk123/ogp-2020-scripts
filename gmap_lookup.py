import csv

import googlemaps


class InvalidPlaceException(Exception):
    def __init__(self, address_string):
        Exception.__init__(self, 'Unknown address: ' + address_string)


class GMapIdLookup:
    def __init__(self, key):
        self.cache = {}
        self.gmaps = googlemaps.Client(key=key)

    def id_of_place(self, address_string):
        if address_string in self.cache:
            return self.cache[address_string]
        result = self.gmaps.geocode(address_string)
        if len(result) == 1:
            if not ('partial_match' in result[0] and result[0]['partial_match']):
                self.cache[address_string] = result[0]['place_id']
                return result[0]['place_id']
        raise InvalidPlaceException(address_string)

    def save_cache(self, path):
        with open(path, 'w') as cache_file:
            for key, value in self.cache:
                cache_file.write(str(key) + ',' + str(value) + '\n')

    def load_cache(self, path):
        with open(path, 'r') as csv_file:
            parsed_csv = csv.reader(csv_file)
            for row in parsed_csv:
                self.cache[row[0]] = row[1]

    def __del__(self):
        self.gmaps.session.close()
