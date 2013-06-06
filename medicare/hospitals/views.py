from django.views import generic as views

from medicare.core.views import NavMixin
from medicare.core.paginator import Paginator
from medicare.hospitals import filtersets, models


class Hospital(NavMixin, views.DetailView):
    """
    A view of a hospital.
    """
    context_object_name = "hospital"
    model = models.Hospital
    section = "hospitals"
    template_name = "hospitals/hospital.html"

    def get_context_data(self, **kwargs):
        context = super(Hospital, self).get_context_data(**kwargs)
        context.update(self.get_additional_context_data())
        return context


class Hospitals(NavMixin, views.ListView):
    """
    A listing of all hospitals.
    """
    context_object_name = "hospitals"
    model = models.Hospital
    paginate_by = 25
    paginator_class = Paginator
    section = "hospitals"
    template_name = "hospitals/hospitals.html"

    def get_context_data(self, **kwargs):
        context = super(Hospitals, self).get_context_data(**kwargs)
        context.update(self.get_additional_context_data())
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        hospital_queryset = super(Hospitals, self).get_queryset().order_by("name")
        self.filterset = filtersets.HospitalFilter(self.request.GET, queryset=hospital_queryset)
        return self.filterset.qs


class Procedure(NavMixin, views.DetailView):
    """
    A view of a procedure.
    """
    context_object_name = "procedure"
    model = models.Procedure
    section = "procedures"
    template_name = "hospitals/procedure.html"

    def get_context_data(self, **kwargs):
        context = super(Procedure, self).get_context_data(**kwargs)
        context.update(self.get_additional_context_data())
        return context


class Procedures(NavMixin, views.ListView):
    """
    A listing of all possible procedures.
    """
    allow_empty = False
    context_object_name = "procedures"
    model = models.Procedure
    paginate_by = None
    section = "procedures"
    template_name = "hospitals/procedures.html"

    def get_context_data(self, **kwargs):
        context = super(Procedures, self).get_context_data(**kwargs)
        context.update(self.get_additional_context_data())
        return context
