#!/usr/bin/python
import os, sys
PATH_APP=os.getcwd()

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

    
import settings 
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"


from virt import models 


# Twisted Stuff
from twisted.internet import reactor, task, ssl
from twisted.web import server, resource

#PyAMF Stuff
from pyamf.remoting.gateway.twisted import TwistedGateway
from pyamf.remoting.gateway import expose_request

# Other things
from datetime import datetime, date



def ScanNodes():

    domainslist = []
    print "Check Date %s" %datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for node in models.Node.objects.all():
        node_, error_ = node.getlibvirt()
        if node_:
            print "%s OK" %node
            for ID in node_.listDomainsID()[1:]:
                domainslist.append(node_.lookupByID(ID).name())
            
            for domain in models.Domain.objects.filter(node=node):
                if domain.name in domainslist:
                    print "%s OK" %domain.name
                else:
                    print "%s Down" %domain.name
                    #
                    # Start domain 
                    #
                    if domain.state != 0:
                        if domain.name == 'dfbsa177':
                            print "Libvirt Create Domain %s" %domain.name
                            #node_.createXML(domain.getxml(),0)
            print 

                    
                    
        else:
            print "%s Down - %s" %(node,error_.get('msg'))
            # migrate all domain node to other node 
            #
            #
    
            
    

class VirtToolService:
    @expose_request
    def live_migrate(self, request, domainid, nodeid):
        domain = None
        dstnode = None
        try:
            domain = models.Domain.objects.get(pk=domainid)
        except models.Domain.DoesNotExist:
            return "Domain not found "
        try:
            dstnode = models.Node.objects.get(pk=nodeid)
        except:
            return "Node not found"
                
        libvirtnodedst, errornodedst = dstnode.getlibvirt()
        libvirtdomain, errordomain = domain.getlibvirt()
        
        if libvirtnodedst and libvirtdomain and domain.node != dstnode:
            migrateok=False
            try:
                libvirtnodedst.migrate(libvirtdomain, models.libvirt.VIR_MIGRATE_LIVE, None, dstnode.hostname, 0)
                migrateok=True
            except:
                migrateok=False
                
            if migrateok == True:
                domain.node = dstnode
                domain.save()
                return "Migration successful"
            else:
                return "Failed migration"    
            
        else:
            return "libvirt to node and / or domain does not respond"
        

def authenticate(username, password):
    print "Authenticating..."
    if username == 'admin' and password == settings.DAEMON_PASSWORD:
        print "Authentication succeeded"
        return True
    else:
        print "Authentication failed"
        return False


if __name__ == '__main__':
    
    print "Libvirt Scanner Started"
    scanner = task.LoopingCall(ScanNodes)
    scanner.start(settings.REFRESH_INTERVAL)    

    gateway = TwistedGateway({'VirtToolService': VirtToolService()}, expose_request=False, authenticator=authenticate)
    root = resource.Resource()
    root.putChild('', gateway)
    try:
        sslContext = ssl.DefaultOpenSSLContextFactory(
                         os.path.join(PATH_APP, 'daemon/cakey.pem'),
                         os.path.join(PATH_APP, 'daemon/cacert.pem'))
    except:
        print "You need some SSL certificates, shutting down..."
        sys.exit()
    reactor.listenSSL(8789, server.Site(root), contextFactory = sslContext)
    reactor.run()
