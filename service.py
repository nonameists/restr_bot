import os
from operator import itemgetter

import googlemaps


class MapService:
    def __init__(self):
        self.token = os.environ.get('GOOGLE_API_TOKEN')
        self.service = googlemaps.Client(key=self.token)

    def get_city_restaurants(self, city):
        try:
            response = self.service.places(city, type='restaurant', language='ru')
            if response['status'] == 'OK':
                addresses = self.formatted_output(response['results'])
                return addresses
            return None

        except Exception:
            raise ValueError

    def get_places_nearby(self, **kwargs):
        kwg = kwargs
        try:
            response = self.service.places_nearby(location=kwg, type='restaurant', language='ru', radius=2000)
            if response['status'] == 'OK':
                addresses = self.formatted_output(response['results'], nearby=True)
                return addresses
            return None

        except Exception:
            raise ValueError

    def formatted_output(self, raw_dict, nearby=False):
        result = []
        address_type = 'formatted_address'
        if nearby:
            address_type = 'vicinity'

        for item in raw_dict[:10]:
            details = self.service.place(item['place_id'])['result']
            result.append(
                {
                    'name': item['name'],
                    'address': ' '.join(item[address_type].split(',')[:2]),
                    'rating': item['rating'],
                    'map': details.get('url'),
                    'website': details.get('website')
                }
            )

        return sorted(result, key=itemgetter('rating'), reverse=True)




