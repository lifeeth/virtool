from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import os 

BASEDIR = os.path.abspath(os.path.dirname(__file__))

urlpatterns = patterns('',

    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'virt.views.home.logout_view', name='sys_logout'),


    # admin
    (r'^admin/', include(admin.site.urls)),
    
    # virttool interface 
    (r'^virt/', include('virt.urls')),
    
    # static files 
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': BASEDIR + '/media/'}),
    
    
)