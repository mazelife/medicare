from django.core.cache import cache
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


class HospitalProcedureQuerySet(models.query.QuerySet):

    CACHE_TTL = 60 * 60 * 24 * 30

    def national_avg_total_payments(self, procedure, state_abbrev="all"):
        cache_key = "avg_total_payments_{0}_{1}".format(state_abbrev, procedure.pk)
        value = cache.get(cache_key)
        if not value:
            filter_kwargs = {"procedure_id": procedure.pk}
            if state_abbrev != "all":
                filter_kwargs["hospital__state__iexact"] = state_abbrev
            value = self.filter(**filter_kwargs).aggregate(avg=models.Avg("avg_total_payments"))["avg"]
            cache.set(cache_key, value, self.CACHE_TTL)
        return value


class HospitalProcedureManager(models.Manager):
    """
    Custom manager for Procedures, using a chained custom queryset.
    """
    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

    def get_query_set(self):
        model = models.get_model('hospitals', 'HospitalProcedure')
        return HospitalProcedureQuerySet(model)


class ProcedureQuerySet(models.query.QuerySet):

    def all_national_avg_total_payments(self):
        self.annotate(avg=models.Avg("hospitalprocedure__avg_total_payments"))


class ProcedureManager(models.Manager):
    """
    Custom manager for Procedures, using a chained custom queryset.
    """
    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

    def get_query_set(self):
        model = models.get_model('hospitals', 'Procedure')
        return ProcedureQuerySet(model)