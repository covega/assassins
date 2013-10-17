from django.conf.urls import patterns, url

from assassins import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^kill$', views.kill, name='kill'),
)
