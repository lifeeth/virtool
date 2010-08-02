import virt 
import libvirt
from django.utils.translation import ugettext as _

#
# libvirt actions 
#

def migrate(domain, dstnode):
            
    libvirtnodedst, errornodedst = dstnode.getlibvirt()
    libvirtdomain, errordomain = domain.getlibvirt()
    
    if libvirtnodedst and libvirtdomain and domain.node != dstnode:
        # change state to wait migrate
        oldstate = domain.state
        domain.state = 97
        domain.save()
        msg_ = ''
        
        try:
            libvirtdomain.migrate(libvirtnodedst, virt.models.libvirt.VIR_MIGRATE_LIVE, None, dstnode.hostname, 0)
            domain.node = dstnode
            domain.state = oldstate
            domain.save()
            msg_ = _("Migration successful")
        except Exception, e:
            msg_ = e
        
        
        # update state from current libvirtdomain
        domain.update_state()
        return msg_ or _("Migration failed")
        
    else:
        return "libvirt to node and / or domain does not respond"



# Resume ( unpause )
def resume(domain):
    libvirtdomain, error_ = domain.getlibvirt()
    if libvirtdomain:
        libvirtdomain.resume()
        domain.state=1
        domain.save()
        return _("Resume OK")
    else:
        return error_ or _("Domain is not running")


# Suspend ( pause )
def suspend(domain):
    libvirtdomain, error_ = domain.getlibvirt()
    if libvirtdomain:
        libvirtdomain.suspend()
        domain.state=3
        domain.save()
        return _("Suspend OK")
    else:
        return error_ or _(" Domain is not running")

# Create
def create(domain, libvirtnode=None):
    
    if libvirtnode:
        try:
            libvirtnode.createXML(domain.getxml(),0)
            domain.state=1
            domain.save()
            return _("Create OK")
        except Exception, e:
            return e
    else:
        libvirtdomain, errordomain = domain.getlibvirt()
        if not libvirtdomain:
            libvirtnode_, error = domain.node.getlibvirt()
            if libvirtnode_:
                try:
                    libvirtnode_.createXML(domain.getxml(),0)
                    domain.state=1
                    domain.save()
                    return _("Create OK")
                except Exception, e:
                    return e
            else:
               return nerror_ or _("Node is not responding") 
        else:
            return _("Domain can not be created because it is running")    
                

# Reboot
def reboot(domain):
    libvirtdomain, error_ = domain.getlibvirt()
    if libvirtdomain:
        libvirtdomain.reboot(0)
        return _("Reboot OK")
    else:
        return error_ or _("Domain is not running")
        

# Shutdown 
def shutdown(domain):
    libvirtdomain, error_ = domain.getlibvirt()
    if libvirtdomain:
        libvirtdomain.shutdown()
        domain.state=96
        domain.save()
        return _("Shutdown OK")
    else:
        return error_ or _("Domain is not running")


#  Destroy 
def destroy(domain):
    libvirtdomain, error_ = domain.getlibvirt()
    if libvirtdomain:
        libvirtdomain.destroy()
        domain.state=96
        domain.save()
        return _("Destroy OK")
    else:
        return error_  or _("Domain is not running")               


# attachDevice
# Create a virtual device attachment to backend.
def attachdevice(device):
    libvirtdomain, error_ = device.domain.getlibvirt()
    if libvirtdomain:
        try:
            libvirtdomain.attachDevice(device.xml)
            return _("Device connected successfully")
        except Exception, e:
            return e            
    else:
        return _("Domain is not running")

    
# detachDevice
# Destroy a virtual device attachment to backend.
def detachdevice(device):
    libvirtdomain, error_ = device.domain.getlibvirt()
    if libvirtdomain:
        try:
            libvirtdomain.detachDevice(device.xml)
            return _("Device disconnected successfully")
        except Exception, e:
            return e            
    else:
        return _("Domain is not running")

        
           
        