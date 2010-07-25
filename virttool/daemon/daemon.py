#!/usr/bin/python
import os, sys
PATH_APP=os.getcwd()

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

    
import settings 
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from virt import models 
from lib.app import virtclient
from django.db.models import F,Q
from datetime import datetime, date

# Twisted 
from twisted.internet import reactor, task, ssl
from twisted.web import server, resource

def CheckNodes():

    domainslist = []
    print "Check Date %s" %datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for node in models.Node.objects.all():
        node_, error_ = node.getlibvirt()
        if node_:
            print "%s OK" %node
            for ID in node_.listDomainsID()[1:]:
                domainslist.append(node_.lookupByID(ID).name())
            
            for domain in models.Domain.objects.filter(Q(node=node),
                                                      ~Q(state__in=[96,97,99])):
                domain.updatestate()
                if domain.name not in domainslist:
                    print "%s Down" %domain.name
                    #
                    # check domain 
                    #
                    if domain.state not in [0,1,2,3,4,95,97]:
                        print "Libvirt creating domain %s" %domain.name
    
                        #virtclient.create(domain,node_)
                        
                        #
                        # developing 
                        #

                    
                    
        else:
            print "%s Down - %s" %(node,error_.get('msg'))
            for d in node.domain_set.filter(~Q(state__in=[95,96,99])):
                # check transport 
                
                
                pass
                
                # migrate all domain node to other node 
                #
                #
    
            


if __name__ == '__main__':
    
    print "Libvirt Scanner Started"
    scanner = task.LoopingCall(CheckNodes)
    scanner.start(settings.REFRESH_INTERVAL)    
    root = resource.Resource()
    reactor.listenTCP(8789, server.Site(root))
    reactor.run()
    
    