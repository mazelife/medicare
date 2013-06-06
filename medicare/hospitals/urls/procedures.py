from django.conf.urls import patterns, url

from medicare.hospitals import views


urlpatterns = patterns('',
    url(r'^$', views.Procedures.as_view(), name="list"),
    url(r'^(?P<pk>\d+)/$', views.Procedure.as_view(), name="detail"),
)