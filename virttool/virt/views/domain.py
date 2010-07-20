from base import * 
from django.utils.translation import ugettext as _
from virt import models 
from virt import forms
from lib.app import virtclient, xmltool


def index(request):
    domainslist=[]    
    for node in models.Node.objects.all().order_by('name'):
        nodelibvirt = node.getlibvirt()
        for domain in models.Domain.objects.filter(node=node):
            domainslist.append(dict(domain=domain,domainlibvirt=domain.getlibvirt(nodelibvirt)))    
            
    paginator = Paginator(domainslist, 200)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    try:
        domainslist_ = paginator.page(page)
    except (EmptyPage, InvalidPage):
        domainslist_ = paginator.page(paginator.num_pages)
        
                
    return render_to_response('virt/domains.html', { 'domains': domainslist_, 'querycount': len(domainslist) }, 
                                context_instance=RequestContext(request))

def add(request):
    if request.method == 'POST':
        form = forms.DomainForm(request.POST)
        if form.is_valid():
            print dir(form)
            print request
            return HttpResponse('OK')
        else:
            return render_to_response('virt/domainadd.html', { 'form' : form },
                                        context_instance=RequestContext(request))
    else:                                    
        domainform = forms.DomainForm()    
        return render_to_response('virt/domainadd.html', { 'form' : domainform },
                                    context_instance=RequestContext(request))

def delete(request,id):
    domain = get_object_or_404(models.Domain, pk=id)
    domain.delete()
    return HttpResponseRedirect(reverse('domain_get'))
    

def edit(request,id):
    domain = get_object_or_404(models.Domain, pk=id)    
    domdict = domain.getdict()
    for f in domain._meta.fields:
        domdict[f.name] = domain.__dict__.get(f.name) 
    domdict['node'] = domain.node.id    
        
    
    form = forms.DomainForm(domdict, instance=domain)
    return render_to_response('virt/domainedit.html', {'domain': domain,
                                                            'form': form }, 
                                                context_instance=RequestContext(request))

def save(request):
    print xmltool.build_domain_xml(request.POST)
    return HttpResponse("ok")
    


#
# libvirt actions 
#
def migrate(request, domainid, nodeid):

    domain = get_object_or_404(models.Domain, pk=domainid)
    node = get_object_or_404(models.Node, pk=nodeid)
    message = virtclient.live_migrate(domain.id,node.id)
    request.user.message_set.create(message=message)
    
    return HttpResponseRedirect(reverse('domain_edit',args=[domain.id]))    
    
    
def resume(request,id):
    domain = get_object_or_404(models.Domain, pk=id)
    libvirtdomain, error_ = domain.getlibvirt()
    if libvirtdomain:
        libvirtdomain.resume()
        request.user.message_set.create(message=_("Resume OK"))
        domain.state=98
        domain.save()
        
    return HttpResponseRedirect(reverse('domain_edit',args=[domain.id]))    
    

def suspend(request, id):
    domain = get_object_or_404(models.Domain, pk=id)
    libvirtdomain, error_ = domain.getlibvirt()
    if libvirtdomain:
        libvirtdomain.suspend()
        request.user.message_set.create(message=_("Suspend OK"))
        domain.state=98
        domain.save()
        
    return HttpResponseRedirect(reverse('domain_edit',args=[domain.id]))         

def create(request,id):
    domain = get_object_or_404(models.Domain, pk=id)
    libvirtdomain, error_ = domain.getlibvirt()
    if not libvirtdomain:
        node_, error_ = domain.node.getlibvirt()
        if node_:
            startok = False
            try:
                node_.createXML(domain.getxml(),0)
                startok = True
                request.user.message_set.create(message=_("Startup OK"))
            except Exception, e:
                request.user.message_set.create(message=e)
                print e
            if startok == True:
                
                domain.state=2
                domain.save()
            
                
    return HttpResponseRedirect(reverse('domain_edit',args=[domain.id]))    

def reboot(request,id):
    domain = get_object_or_404(models.Domain, pk=id)
    libvirtdomain, error_ = domain.getlibvirt()
    if libvirtdomain:
        libvirtdomain.reboot()
        request.user.message_set.create(message=_("Reboot OK"))
        domain.state=98
        domain.save()

    return HttpResponseRedirect(reverse('domain_edit',args=[domain.id]))
    
                    
def shutdown(request,id):
    domain = get_object_or_404(models.Domain, pk=id)
    libvirtdomain, error_ = domain.getlibvirt()
    if libvirtdomain:
        libvirtdomain.shutdown()
        request.user.message_set.create(message=_("Shutdown OK"))
        domain.state=98
        domain.save()
        
    return HttpResponseRedirect(reverse('domain_edit',args=[domain.id]))    


def destroy(request,id):
    domain = get_object_or_404(models.Domain, pk=id)
    domain_, error_ = domain.getlibvirt()
    if domain_:
        domain_.destroy()
        request.user.message_set.create(message=_("Destroy OK"))
        domain.state=98 
        domain.save()
     
    return HttpResponseRedirect(reverse('domain_edit',args=[domain.id]))   
    





