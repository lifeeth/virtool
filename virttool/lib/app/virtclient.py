import virt 

def live_migrate(domainid, nodeid):
    
    domain = None
    dstnode = None
    
    try:
        domain = virt.models.Domain.objects.get(pk=domainid)
    except virt.models.Domain.DoesNotExist:
        return "Domain not found "
    try:
        dstnode = virt.models.Node.objects.get(pk=nodeid)
    except:
        return "Node not found"
            
    libvirtnodedst, errornodedst = dstnode.getlibvirt()
    libvirtdomain, errordomain = domain.getlibvirt()
    
    if libvirtnodedst and libvirtdomain and domain.node != dstnode:
        # change state to wait migrate
        domain.state = 97
        domain.save()
        
        migrateok=False
        msginfo=''
        
        try:
            libvirtnodedst.migrate(libvirtdomain, virt.models.libvirt.VIR_MIGRATE_LIVE, None, dstnode.hostname, 0)
            migrateok=True
        except:
            migrateok=False
            
        if migrateok == True:
            domain.node = dstnode
            domain.save()
            msginfo="Migration successful"
        else:
            msginfo="Failed migration"   
        
        # update state from current libvirtdomain
        libvirtdomain, errordomain = domain.getlibvirt()
        if libvirtdomain:
            domain.state = libvirtdomain.info()[0]
        else:
            domain.state =  99
        
        domain.save()
        return msginfo
        
    else:
        return "libvirt to node and / or domain does not respond"



        