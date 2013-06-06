import django_filters

from medicare.hospitals.models import Hospital


class HospitalFilter(django_filters.FilterSet):

    city = django_filters.CharFilter(lookup_type='icontains')
    name = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = Hospital
        fields = ['state', 'city', 'name']

    def __init__(self, *args, **kwargs):
        super(HospitalFilter, self).__init__(*args, **kwargs)
        self.filters['name'].label = u"Hospital name"
        all_states = self.filters['state'].extra['choices']
        self.filters['state'].extra['choices'] = (('', "Any state"),) + all_states
