from operator import itemgetter

from django.core.urlresolvers import reverse
from django.db import connection, models

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

    def get_absolute_url(self):
        return reverse("hospitals:detail", args=None, kwargs={'pk': self.id})

    def procedures(self):
        """
        Annotates the queryset of hospitals procedures with the national average for each
        procedure.
        """
        return Procedure.objects.filter(hospitalprocedure__hospital_id=self.id)


class Procedure(models.Model):
    """
    A model of a procedure.
    """
    name = models.CharField(db_index=True, max_length=255)

    objects = managers.ProcedureManager()

    def __unicode__(self):
        return self.name

    def averages(self, state=None):
        """
        Provide the national or state-level averages for the given procedure for:

            1. Number of discharges
            2. Average reimbursement
            3. Average charge by hospital

        """
        if state:
            queryset = self.hospitalprocedure_set.filter(hospital__state=state)
        else:
            queryset = self.hospitalprocedure_set
        fields = ('avg_covered_charges', 'avg_total_payments', 'discharges')
        aggregates = (models.Avg(f) for f in fields)
        result = queryset.aggregate(*aggregates)
        return dict((f, result[f + "__avg"]) for f in fields)

    def get_absolute_url(self):
        return reverse("procedures:detail", args=None, kwargs={'pk': self.id})

    def range(self):
        return self.hospitalprocedure_set.aggregate(
            min=models.Max("avg_total_payments"),
            max=models.Min("avg_total_payments")
        )


class HospitalProcedure(models.Model):
    """
    A model of a specific procedure data done by a hospital.
    """
    hospital = models.ForeignKey("Hospital")
    procedure = models.ForeignKey("Procedure")
    discharges = models.IntegerField()
    avg_covered_charges = models.DecimalField(
        decimal_places=3,
        help_text=(
            "The average amount for which the hopistal is reimbursed "
            "by Medicare for this procedure."
        ),
        max_digits=10
    )
    avg_total_payments = models.DecimalField(
        decimal_places=3,
        help_text="The average price this hospital charges for this procedure",
        max_digits=10
    )

    objects = managers.HospitalProcedureManager()

    class Meta:
        unique_together = ("hospital", "procedure")

    def __unicode__(self):
        return unicode(self.procedure)
