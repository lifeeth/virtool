import virt 
from django.utils.translation import ugettext as _

#
# libvirt actions 
#

def migrate(domain, dstnode):
            
    libvirtnodedst, errornodedst = dstnode.getlibvirt()
    libvirtdomain, errordomain = domain.getlibvirt()
    
    if libvirtnodedst and libvirtdomain and domain.node != dstnode:
        # change state to wait migrate
        domain.state = 97
        domain.save()
        msg_ = ''
        
        try:
            libvirtnodedst.migrate(libvirtdomain, virt.models.libvirt.VIR_MIGRATE_LIVE, None, dstnode.hostname, 0)
            domain.node = dstnode
            domain.save()
            msg_ = _("Migration successful")
        except Exception, e:
            msg_ = e
        
        # update state from current libvirtdomain
        libvirtdomain, errordomain = domain.getlibvirt()
        if libvirtdomain:
            domain.state = libvirtdomain.info()[0]
        else:
            domain.state =  99
        
        domain.save()
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
def create(domain):
    libvirtdomain, error_ = domain.getlibvirt()
    # check libvirt Domain 
    if not libvirtdomain:
        node_, nerror_ = domain.node.getlibvirt()        
        if node_:
            try:
                node_.createXML(domain.getxml(),0)
                domain.state=1
                domain.save()
                return _("Create OK")
            except Exception, e:
                return e
        else:
            return nerror_
    else:
        return _("Domain is not created because libvirt domain is running")    
                

# Reboot
def reboot(domain):
    libvirtdomain, error_ = domain.getlibvirt()
    if libvirtdomain:
        libvirtdomain.reboot(0)
        return _("Reboot OK")
    else:
        return error_ or _("Domain can not be restarted because it is not running")
        

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
        return error_  or _("Domain can not be destroyed because it is not running")               

        