from base import * 
from django.utils.translation import ugettext as _
from virt import models 
from virt import forms
from lib.app import virtclient, xmltool
from django.db.models import F,Q


def index(request):
    
    # query search 
    querys = None
    query = request.GET.get('q', '')
    if query:
        query = query.strip()
        
    domainslist=[]   
    for node in models.Node.objects.filter(Q(domain__name__icontains=query) | \
                                           Q(domain__description__icontains=query)).order_by('name') if query else \
                models.Node.objects.all().order_by('name'):
        if node.active == True:
            libvirtnode, error_ = node.getlibvirt()
        else:
            libvirtnode, error_ = None,None
        for domain in node.domain_set.filter(Q(name__icontains=query) | \
                                             Q(description__icontains=query)) if query else node.domain_set.all():
            domainslist.append(dict(domain=domain,libvirtdomain=domain.getlibvirt(libvirtnode) if libvirtnode else None))    
            
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
            newdomain = form.save()
            newdomain.xml = xmltool.build_domain_xml(request.POST)
            newdomain.save()
            request.user.message_set.create(message=_("Domain registered successfully"))
            return HttpResponseRedirect(reverse('domain_get'))
        else:
            return render_to_response('virt/domainadd.html', { 'form' : form },
                                        context_instance=RequestContext(request))
    else:                                    
        form = forms.DomainForm()   
        return render_to_response('virt/domainadd.html', { 'form' : form },
                                    context_instance=RequestContext(request))

def delete(request,id):
    domain = get_object_or_404(models.Domain, pk=id)
    domain.delete()
    request.user.message_set.create(message=_("Domain successfully removed"))
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
    domain = get_object_or_404(models.Domain, pk=request.POST.get('id'))
    form = forms.DomainForm(request.POST,instance=domain)
    if form.is_valid():
        currentdomain = form.save()
        currentdomain.xml = xmltool.build_domain_xml(request.POST)
        currentdomain.save()
        request.user.message_set.create(message=_("Domain successfully changed"))
    else:
        return render_to_response('virt/domainedit.html', {'form': form ,
                                                           'domain': domain },
                                    context_instance=RequestContext(request))
        
    return HttpResponseRedirect(reverse('domain_edit',args=[domain.id]))
    


#
# libvirt actions 
#
def migrate(request, domainid, nodeid):
    domain = get_object_or_404(models.Domain, pk=domainid)
    node = get_object_or_404(models.Node, pk=nodeid)
    message = virtclient.migrate(domain,node)
    request.user.message_set.create(message=message)
    return HttpResponseRedirect(reverse('domain_edit',args=[domain.id]))    
    
    
def resume(request,id):
    domain = get_object_or_404(models.Domain, pk=id)
    message = virtclient.resume(domain)
    request.user.message_set.create(message=message)
    return HttpResponseRedirect(reverse('domain_edit',args=[domain.id]))    
    

def suspend(request, id):
    domain = get_object_or_404(models.Domain, pk=id)
    message = virtclient.suspend(domain)
    request.user.message_set.create(message=message)
    return HttpResponseRedirect(reverse('domain_edit',args=[domain.id]))         


def create(request,id):
    domain = get_object_or_404(models.Domain, pk=id)
    message = virtclient.create(domain)
    request.user.message_set.create(message=message)
    return HttpResponseRedirect(reverse('domain_edit',args=[domain.id]))
    
    
def reboot(request,id):
    domain = get_object_or_404(models.Domain, pk=id)
    message = virtclient.reboot(domain)
    request.user.message_set.create(message=message)
    return HttpResponseRedirect(reverse('domain_edit',args=[domain.id]))
                    
def shutdown(request,id):
    domain = get_object_or_404(models.Domain, pk=id)
    message = virtclient.shutdown(domain)
    request.user.message_set.create(message=message)
    return HttpResponseRedirect(reverse('domain_edit',args=[domain.id]))
    
def destroy(request,id):
    domain = get_object_or_404(models.Domain, pk=id)
    message = virtclient.destroy(domain)
    request.user.message_set.create(message=message)
    return HttpResponseRedirect(reverse('domain_edit',args=[domain.id]))
    
