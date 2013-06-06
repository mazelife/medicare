from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^hospitals/', include('medicare.hospitals.urls.hospitals', namespace="hospitals")),
    url(r'^procedures/', include('medicare.hospitals.urls.procedures', namespace="procedures")),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
