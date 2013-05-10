from django.db import models


class HospitalQuerySet(models.query.QuerySet):

    def not_geocoded(self):
        """
        Returns a queryset of models that have not been geocoded (i.e. do not
        have a latitude, longitude, or geohash).
        """
        query = models.Q(latitude=None) | models.Q(longitude=None) | models.Q(geohash=None)
        return self.filter(query)


class HospitalManager(models.Manager):
    """
    Custom manager for hospitals, using a chained custom queryset.
    """
    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

    def get_query_set(self):
        model = models.get_model('hospitals', 'Hospital')
        return HospitalQuerySet(model)
