from django.db import models

from django_localflavor_us import models as us_models

from medicare.hospitals import managers


class Hospital(models.Model):
    """
    A model of a hospital.
    """
    name = models.CharField(db_index=True, max_length=255)
    address = models.TextField("Street address")
    city = models.CharField(max_length=100)
    state = us_models.USStateField()
    zipcode = models.CharField(max_length=10)
    region = models.CharField(max_length=50)
    latitude = models.DecimalField(
        decimal_places=6,
        max_digits=9,
        null=True
    )
    longitude = models.DecimalField(
        decimal_places=6,
        max_digits=9,
        null=True
    )
    geohash = models.CharField(
        blank=True,
        db_index=True,
        max_length=12
    )

    objects = managers.HospitalManager()

    def __unicode__(self):
        return self.name


class Procedure(models.Model):
    """
    A model of a procedure.
    """
    name = models.CharField(db_index=True, max_length=255)

    def __unicode__(self):
        return self.name


class HospitalProcedure(models.Model):
    """
    A model of a specific procedure data done by a hospital.
    """
    hospital = models.ForeignKey("Hospital")
    procedure = models.ForeignKey("Procedure")
    discharges = models.IntegerField()
    avg_covered_charges = models.DecimalField(decimal_places=3, max_digits=10)
    avg_total_payments = models.DecimalField(decimal_places=3, max_digits=10)

    class Meta:
        unique_together = ("hospital", "procedure")

    def __unicode__(self):
        return u"{0} - {1}".format(self.hospital, self.procedure)
