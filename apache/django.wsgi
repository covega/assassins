import os
import sys

apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)

workspace = os.path.dirname(project)
sys.path.append(workspace)
sys.path.append('/usr/lib/python2.5/site-packages/django/')
sys.path.append('/home/pi/django_projects/assassins_project/assassins_site')
os.environ['DJANGO_SETTINGS_MODULE'] = 'assassins_site.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()