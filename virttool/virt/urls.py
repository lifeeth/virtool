from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'virt.views.home.index', name="home"),
    
    # Node 
    url(r'^node/$', 'virt.views.node.index', name="node_get"),
    url(r'^node/add/$', 'virt.views.node.add', name="node_add"),    
    url(r'^node/(\d+)/$', 'virt.views.node.edit', name="node_edit"),  
    url(r'^node/(\d+)/updatedomains/$', 'virt.views.node.updatedomains', name="node_updatedomains"),  
    url(r'^node/(\d+)/updatecapabilities/$', 'virt.views.node.updatecapabilities', name="node_updatecapabilities"),
    
    url(r'^node/(\d+)/delete/$', 'virt.views.node.delete', name="node_delete"),       
    url(r'^node/save/$', 'virt.views.node.save', name="node_save"),    
    
    # Domain
    url(r'^domain/$', 'virt.views.domain.index', name="domain_get"),
    url(r'^domain/add/$', 'virt.views.domain.add', name="domain_add"),    
    url(r'^domain/(\d+)/$', 'virt.views.domain.edit', name="domain_edit"),  
    url(r'^domain/(\d+)/delete/$', 'virt.views.domain.delete', name="domain_delete"),
    url(r'^domain/save/$', 'virt.views.domain.save', name="domain_save"),
    
    # Device
    url(r'^domain/(\d+)/device/(\w+)/add/$', 'virt.views.device.add', name="device_add"),
    url(r'^device/(\d+)/$', 'virt.views.device.edit', name="device_edit"),
    url(r'^device/(\d+)/attach/$', 'virt.views.device.attachdevice', name="device_attach"),
    url(r'^device/(\d+)/detach/$', 'virt.views.device.detachdevice', name="device_detach"),
    
    url(r'^device/(\d+)/delete/$', 'virt.views.device.delete', name="device_delete"),
    url(r'^device/save/$', 'virt.views.device.save', name="device_save"),
    
    
    
    
    # libvirt domain actions 
    url(r'^domain/(\d+)/migrate/(\d+)/$', 'virt.views.domain.migrate', name="domain_migrate"),
    url(r'^domain/(\d+)/create/$', 'virt.views.domain.create', name="domain_create"),
    url(r'^domain/(\d+)/resume/$', 'virt.views.domain.resume', name="domain_resume"),
    url(r'^domain/(\d+)/suspend/$', 'virt.views.domain.suspend', name="domain_suspend"),
    url(r'^domain/(\d+)/reboot/$', 'virt.views.domain.reboot', name="domain_reboot"),
    url(r'^domain/(\d+)/shutdown/$', 'virt.views.domain.shutdown', name="domain_shutdown"),
    url(r'^domain/(\d+)/destroy/$', 'virt.views.domain.destroy', name="domain_destroy"),
      
    
    

)