import decimal
from operator import attrgetter
from optparse import make_option
import time

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError

import geohash
import requests

from medicare.hospitals.models import Hospital


class Command(BaseCommand):
    """
    A management command that uses Bing's Geocoding service to look up coordinates for
    hospitals based on their address.
    """

    address_fields = ("name", "address", "city", "state", "zipcode")
    api_url = "http://dev.virtualearth.net/REST/v1/Locations"
    failed_lookups = []
    option_list = BaseCommand.option_list + (
        make_option("--reset",
                    action='store_true',
                    dest='reset',
                    default=False,
                    help="Geocode all schools, even ones with existing data."
                    ),
    )
    sleep_time = 0.5

    def __init__(self, *args, **kwargs):
        self.help = self.__doc__
        if not hasattr(settings, "BING_GEOCODE_API_KEY"):
            raise ImproperlyConfigured('The "BING_GEOCODE_API_KEY" setting is missing.')
        else:
            self.api_key = settings.BING_GEOCODE_API_KEY
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, reset=False, *args, **kwargs):
        if reset:
            base_qs = Hospital.objects
        else:
            base_qs = Hospital.objects.not_geocoded()
        self.hospitals_queryset = base_qs.only(*self.address_fields).order_by("name")
        if not self.confirm():
            return
        for args in self.get_addresses():
            hospital_id, coords, err = self.geocode_address(*args)
            if err:
                self.failed_lookups.append((hospital_id, err))
            else:
                hospital = Hospital.objects.get(pk=hospital_id)
                hospital.latitude = coords[0]
                hospital.longitude = coords[1]
                hospital.geohash = geohash.encode(*coords, precision=12)
                try:
                    hospital.save()
                except decimal.InvalidOperation, e:
                    raise CommandError(e)
                ascii_name = self.name_lookup[hospital_id].encode('ascii', 'ignore')
                self.stdout.write("Coordinates added for {0}.\n".format(ascii_name))
            # Avoid spamming the API.
            time.sleep(self.sleep_time)
        self.stdout.write("*" * 60 + "\n")
        self.stdout.write("The follwing lookups failed:\n")
        for hospital_id, err in self.failed_lookups:
            ascii_name = self.name_lookup[hospital_id].encode('ascii', 'ignore')
            self.stdout.write("[{0}] {1} - Reason: {2}\n".format(
                hospital_id, ascii_name, err
            ))

    def get_addresses(self):
        self.name_lookup = {}
        getters = map(attrgetter, ("pk", "zipcode", "state", "city", "address"))
        for hospital in self.hospitals_queryset:
            self.name_lookup[hospital.pk] = hospital.name
            yield (f(hospital) for f in getters)

    def geocode_address(self, hospital_id, zipcode, state, city, address_string):
        request = requests.get(self.api_url, params={
            'countryRegion': 'us',
            'postalCode': zipcode,
            'adminDistrict': state,
            'locality': city,
            'addressLine': address_string,  # The address to lookup
            'maxResults': "1",
            'key': self.api_key,  # The API key
            'flags': 'j'  # Return data in JSON format
        })
        try:
            if not request.status_code == 200:
                raise requests.exceptions.RequestException("Bad request")
            if not request.json:
                raise requests.exceptions.RequestException("No JSON")
            try:
                results = request.json['resourceSets'][0]['resources'][0]
            except (IndexError, TypeError):
                raise requests.exceptions.RequestException("Unexpected response format.")
            # If the quality of the lookup is low, it should be discarded.
            # This means that the API was unable to use a portion of the address string.
            if results["confidence"] == u"Low":
                raise requests.exceptions.RequestException("Low confidence")
            try:
                lat, lon = results['point']['coordinates']
                latitude = decimal.Decimal(lat)
                longitude = decimal.Decimal(lon)
            except decimal.InvalidOperation:
                raise requests.exceptions.RequestException("Bad decimal format")
        except requests.exceptions.RequestException, exc:
            return (hospital_id, None, str(exc))
        else:
            return (hospital_id, (latitude, longitude), None)

    def confirm(self):
        count = self.hospitals_queryset.count()
        est_seconds = count * (1 + self.sleep_time)
        if est_seconds < 60:
            est_minutes = "less than a minute"
        else:
            est_minutes = "about {0} minutes".format(int(est_seconds / 60))
        self.stdout.write(self.__doc__ + "\n")
        self.stdout.write("*" * 60 + "\n")
        confirm = raw_input((
            "Bing limits you to 10,000 requests per day. "
            "{0} hospitals will be geocoded in this session. "
            "That will take {1}."
            "Continue? (yes|no) "
        ).format(count, est_minutes)).lower()
        if confirm != "yes":
            self.stdout.write("Stopping session.\n")
            return False
        return True
