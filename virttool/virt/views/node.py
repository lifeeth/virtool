from base import * 
from django.utils.translation import ugettext as _
from virt import models, forms

def index(request):
    
    nodelist = [ dict(node=node, nodelibvirt=node.getlibvirt()) for node in models.Node.objects.all() ]
    paginator = Paginator(nodelist, 200)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    try:
        nodelist_ = paginator.page(page)
    except (EmptyPage, InvalidPage):
        nodelist_ = paginator.page(paginator.num_pages)
        
    return render_to_response('virt/nodes.html', { 'nodes': nodelist_ }, 
                                context_instance=RequestContext(request))
                                
                                
def add(request):
    if request.method == 'POST':
        # add new node 
        form = forms.NodeForm(request.POST)
        if form.is_valid():
            newnode = models.Node()
            fnode = forms.NodeForm(request.POST,instance=newnode)          
            fnode.save()
    
            # getting libvirt virConnect instance to optimize register
            libvirtnode = newnode.getlibvirt()
    
            # update capabilities, name, state from libvirt 
            newnode.update_capabilities(libvirtnode=libvirtnode)
    
            # import all domains from libvirt Node
            if request.POST.get('importdomains'):
                newnode.import_domains(libvirtnode=libvirtnode)  
            
            request.user.message_set.create(message=_("Node registered successfully"))
            return HttpResponseRedirect(reverse('node_get'))
        else:
            return render_to_response('virt/nodeadd.html', {'form': form, 'URIHELP': models.DRIVERS_DESCRIPTION },
                                        context_instance=RequestContext(request))
    else:
                                        
        form = forms.NodeForm()
        return render_to_response('virt/nodeadd.html', {'form': form, 'URIHELP': models.DRIVERS_DESCRIPTION },
                                            context_instance=RequestContext(request))


def edit(request,id):
    node = get_object_or_404(models.Node, pk=id)
    form = forms.NodeForm(instance=node)    
    return render_to_response('virt/nodeedit.html', {'form': form, 'node': node, 'URIHELP': models.DRIVERS_DESCRIPTION }, 
                                        context_instance=RequestContext(request))    

def delete(request,id):
    node = get_object_or_404(models.Node, pk=id)
    node.delete()
    request.user.message_set.create(message=_("Node successfully removed"))
    return HttpResponseRedirect(reverse('node_get'))
    

def updatedomains(request,id):
    node = get_object_or_404(models.Node, pk=id)
    node.import_domains()   
    form = forms.NodeForm(instance=node)   
    request.user.message_set.create(message=_("Domains imported Node %s" %node.name ))
    return HttpResponseRedirect(reverse('node_edit',args=[node.id]))
    
def updatecapabilities(request,id):
    node = get_object_or_404(models.Node, pk=id)
    node.update_capabilities()
    request.user.message_set.create(message=_("Updated Capabilities"))  
    return HttpResponseRedirect(reverse('node_edit',args=[node.id]))  
    
    
def save(request):
    node = get_object_or_404(models.Node, pk=request.POST.get('id'))
    form = forms.NodeForm(request.POST,instance=node)   
    if form.is_valid():
        form.save()
        request.user.message_set.create(message=_("Node successfully changed"))
    else:
        return render_to_response('virt/nodeedit.html', {'form': form ,
                                                              'node': node },
                                    context_instance=RequestContext(request))
    return HttpResponseRedirect(reverse('node_get'))
    
    
