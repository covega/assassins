from django.conf.urls import patterns, url

from assassins import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^kill$', views.kill, name='kill'),
                       url(r'^confirm_kill$', views.confirm_kill, name='confirm_kill'),
)
