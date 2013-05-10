from django.contrib import admin
from medicare.hospitals import models


class HospitalProcedureInline(admin.StackedInline):
    extra = 1
    model = models.HospitalProcedure
    ordering = ("hospital", "procedure", )


class HospitalAdmin(admin.ModelAdmin):
    inlines = [HospitalProcedureInline]
    list_display = ("name", "city", "state")
    list_filter = ("state",)
    search_fields = ("name", "city",)


class ProcedureAdmin(admin.ModelAdmin):
    ordering = ("name", )


admin.site.register(models.Hospital, HospitalAdmin)


admin.site.register(models.Procedure, ProcedureAdmin)
