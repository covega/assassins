from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings

from assassins import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^kill$', views.kill, name='kill'),
    url(r'^confirm_kill$', views.confirm_kill, name='confirm_kill'),
    url(r'^submit_registration$', views.submit_registration, name='submit_registration'),
    #url(r'^status$', views.status, name='status'),
    url(r'^admin/', views.admin, name='admin'),
    url(r'^update_dorm_info$', views.update_dorm_info, name='update_dorm_info'),
)
