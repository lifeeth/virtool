from django.db import models
from django.db.models import F,Q
import libvirt
from lib.app import snmp, xmltool
from django.utils.translation import ugettext as _
from constants import * 
import fields
import settings

class Node(models.Model):    
    
    name = models.CharField(_('Name'), max_length=100, unique=True)
    
    def __unicode__(self):
        return self.name
        
    hostname = models.CharField(_('Hostname'), null=True, blank=True, max_length=255)
    uri = models.CharField(_('URI'), max_length=255, null=True, blank=True, default=None)
    description = models.CharField(_('Description'), blank=False, max_length=255)
    type = models.IntegerField(_('Node Type'), default=0, choices=VIRT_INTERFACE_NAME)
    state = models.IntegerField(default=0, choices=NODE_STATE)
    capabilities = models.TextField(null=True,blank=True)
    defaultbridge = models.CharField(_('Bridge Default'), max_length=50, null=True, blank=True, default=None)
    active = models.BooleanField(_('Active'), default=True,null=False)
    datecreated = models.DateTimeField(auto_now_add=True, null=False)
    datemodified = models.DateTimeField(auto_now=True, null=False)
    
    
    def getlibvirt(self):
        """
          Return instance libvirt.virConnect and 
          dict(libvirt.libvirtError[code,message])
        """
        URI = self.uri or VIRT_INTERFACE_URI[self.type] %self.hostname
        try:
            return libvirt.open(URI), None                       
        except libvirt.libvirtError, le:
            return None, dict(code=le.get_error_code(), msg=le.get_error_message())
    
    
    def update_capabilities(self,autosave=True,libvirtnode=None):
        """
          Update name, capabilities, state from libvirt 
        """
        node_, error_ = libvirtnode or self.getlibvirt()
        if node_:
            self.capabilities = node_.getCapabilities()
            self.state = 1
        else:
            self.state = 2
            
        if autosave == True:
            self.save()

            
    def getnetdev(self,version=1,community="public"):
        """
          Get network interfaces via SNMP 
        """
        snmp_ = snmp.Snmp()
        devlist = []
        NOTLISTED=['vif','lo']
        
        for dev in snmp_.snmpwalk(self.hostname,"1.3.6.1.2.1.2.2.1.2",version,community):
            invalidfound = False
            for nl in NOTLISTED:
                if dev.split('STRING:')[1].strip().startswith(nl):
                    invalidfound=True
            if invalidfound == False:
                devlist.append(dev.split('STRING:')[1].strip())
        return devlist
                    

    def import_domains(self,libvirtnode=None):
        """
          Import all domains from Node 
        """        
        node_, erro_ = libvirtnode or self.getlibvirt()

        if node_:
            libvirtdomains = [ node_.lookupByID(ID) for ID in node_.listDomainsID()[1:] ]
            domainlist = [ domain_.name for domain_ in Domain.objects.all() ]
            for libvirtdomain in libvirtdomains:
                if libvirtdomain.name() not in domainlist:
                    new_domain = Domain()
                    new_domain.name=libvirtdomain.name()
                    new_domain.description='Virtual Machine %s' %libvirtdomain.name()
                    new_domain.node=self
                    new_domain.state=libvirtdomain.info()[0]
                    
                    if self.defaultbridge:
                        options = dict(defaultbridge=self.defaultbridge)
                    else:
                        options = None
                        
                    xmlf = xmltool.getxml(libvirtdomain.XMLDesc(0), options)
                    new_domain.type = xmlf.get('type')
                    new_domain.xml= xmlf.get('domain')
                    new_domain.save()
                    for d in xmlf.get('devices'):
                        new_device = Device()
                        new_device.domain = new_domain
                        new_device.type = d.get('type')
                        new_device.xml = d.get('xml')
                        new_device.save()

                #else:
                #    existing_domain = Domain.objects.get(name=libvirtdomain.name())
                #    existing_domain.state = libvirtdomain.info()[0]
                #    existing_domain.xml= xmltool.formatxml(libvirtdomain.XMLDesc(0))
                #    existing_domain.save()
                        
    
                        
    class Meta:
        ordering = 'name',
        verbose_name = _('Node')
        verbose_name_plural = (_('Nodes'))
        


class Domain(models.Model):

    node = models.ForeignKey(Node, verbose_name=_('Node'))
    name = models.CharField(_('Name'), max_length=100)
    uuid = models.CharField(_('UUID'), max_length=36,blank=True)
    hostname = models.CharField(_('Host'), max_length=200, blank=True, null=True, default=None)
    description = models.CharField(_('Description'), blank=False, max_length=200)
    type = models.CharField(_('Type'), max_length=20, choices=DOM_TYPES)
    xml = models.TextField(_('XML'))
    autostart = models.BooleanField(_('Auto start'), default=True)
    priority = models.IntegerField(_('Priority'), default=10)    
    state = models.IntegerField(default=0, choices=DOMAIN_STATE)
    datecreated = models.DateTimeField(auto_now_add=True, null=False)
    datemodified = models.DateTimeField(auto_now=True, null=False)
    
    
    def getlibvirt(self,libvirtnode=None):
        """
          Return Domain libvirt
        """       
        node_, error_ = libvirtnode or self.node.getlibvirt()
        try:    
            return node_.lookupByName(self.name), error_
        except:
            return None, error_
            
    
    def updatestate(self):
        """
           Update state Domain 
        """
        if self.state not in [96,97,99]:   
            change=False         
            state = self.state
            domain_, error_ = self.getlibvirt()
            if domain_:
                state_ = domain_.info()[0]
                if state_ != state:
                    change=True
                    self.state = state_
            else:
                self.state = 98
                change=True
                
            if change == True:
                self.save()
    
    
    #
    #  GETs Devices 
    #
    
    def getemulator(self):
        return self.device_set.filter(type='emulator')
    def getdisk(self):
        return self.device_set.filter(type='disk')                            
    def getinterface(self):
        return self.device_set.filter(type='interface')        
    def getgraphics(self):
        return self.device_set.filter(type='graphics')
    def getinput(self):
        return self.device_set.filter(type='input')
    def getconsole(self):
        return self.device_set.filter(type='console')
    def getserial(self):
        return self.device_set.filter(type='serial')
    def getparallel(self):
        return self.device_set.filter(type='parallel')
    def getchannel(self):
        return self.device_set.filter(type='channel')    
    
    
    def getdict(self):
        """
           Return Domain dictionary python 
        """
        return xmltool.get_domain_dict(self.xml)
                    
    
    def getxml(self):
        """
           Return Domain XML Format 
        """
        
        xmldomain = str()
        xmldomain = self.xml

        xmldomain = xmldomain.replace('</domain>','')
        xmldomain+="<devices>\n"
        for devicetype in ['emulator',
                           'disk',
                           'interface',
                           'graphics',
                           'input',
                           'parallel',
                           'serial',
                           'console',
                           'channel',
                           'sound',
                           'video',
                           'hostdev']:
            for dxml in self.device_set.filter(type=devicetype):
                xmldomain+="%s\n" %dxml.xml
        xmldomain+="</devices>\n</domain>"

        return xmldomain
            
    
    def __unicode__(self):
        return self.name 
        
        
    class Meta:
        ordering = 'name',
        verbose_name = _('Domain')
        verbose_name_plural = (_('Domains'))

        
#
#  Transport Domain
#
class Transport(models.Model):
    node = models.ForeignKey(Node, verbose_name=_('Node'))
    domain = models.ForeignKey(Domain, verbose_name=_('Domain'))

    def __unicode__(self):
        return "%s %s" %(self.node, self.domain)

    class Meta:
        ordering = 'node',
        verbose_name = _('Transport')
        verbose_name_plural = (_('Transport List'))

#
# Devices
#
class Device(models.Model):
    
    domain = models.ForeignKey(Domain, verbose_name=_('Domain'))
    description = models.CharField(_('Description'), max_length=255, null=True, blank=True, default=None)
    type = models.CharField(_('Device Type'), max_length=50, choices=DEVICE_TYPES)  
    xml = models.TextField(_('XML'))
    
    def __unicode__(self):
        return "%s - %s : %s" %(self.domain,self.type,self.description)
    
    def getdict(self):
        """
           Return Device dictionary python
        """
        return xmltool.get_device_dict(self.xml)
    
                
    class Meta:
        ordering = 'type',
        verbose_name = _('Device')
        verbose_name_plural = (_('Devices'))

