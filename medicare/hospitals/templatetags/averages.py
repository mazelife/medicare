from django.core.exceptions import ImproperlyConfigured
from django import template

from medicare.hospitals.models import HospitalProcedure


register = template.Library()


@register.simple_tag()
def average(procedure):
    return HospitalProcedure.objects.national_avg_total_payments(procedure)
