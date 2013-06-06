from django.conf.urls import patterns, url

from medicare.hospitals import views


urlpatterns = patterns('',
    url(r'^$', views.Hospitals.as_view(), name="list"),
    url(r'^(?P<pk>\d+)/$', views.Hospital.as_view(), name="detail"),
)
