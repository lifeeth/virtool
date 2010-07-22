from base import * 
from django.utils.translation import ugettext as _
from virt import models 
from virt import forms
from lib.app import virtclient, xmltool, libvirttemplate


    
def getformdevice(typedev):
    tdev = typedev
    
    if tdev in models.DEVICE_TYPE_LIST:
        if tdev == 'disk':
            return forms.DiskForm
        elif tdev == 'interface':
            return forms.InterfaceForm
        elif tdev == 'graphics':
            return forms.GraphicsForm
        elif tdev == 'input':
            return forms.InputForm
        elif tdev in ['console','serial','parallel']:
            return forms.CSPForm
        elif tdev == 'emulator':
            return forms.EmulatorForm
        else:
            return forms.GenericDeviceForm
                 
         
def add(request, domainid, typedevice):
    domain = get_object_or_404(models.Domain, pk=domainid)  
        
    if request.method == 'POST':
        getform = getformdevice(typedevice)
        device_ = models.Device()
        device_.domain = domain
        device_.type = typedevice
        form = getform(request.POST,instance=device_)
        
        if form.is_valid():
            newdevice = form.save()
            
            xml_desc = xmltool.build_device_xml(request.POST)
            if len(xml_desc) > 5:
                newdevice.xml = xml_desc
                newdevice.save()
            else:
                newdevice.delete()
                    
            request.user.message_set.create(message=_("Device registered successfully"))
            return HttpResponseRedirect(reverse('domain_edit',args=[domain.id]))
            
        else:
            macxen=""
            try:
                maxxen=libvirttemplate.maxxen()[0]
            except:
                pass
                
            return render_to_response('virt/deviceadd.html', { 'form' : form, 'domain': domain, 'type': typedevice, 'macxen': macxen },
                                      context_instance=RequestContext(request))

    else:    
        device_ = models.Device()
        device_.domain = domain
        device_.type = typedevice
        getform = getformdevice(typedevice)
        form = getform(instance=device_)
        return render_to_response('virt/deviceadd.html', { 'form' : form, 'domain': domain, 'type': typedevice },
                                        context_instance=RequestContext(request))
            
            
def edit(request,id):
    device = get_object_or_404(models.Device, pk=id)    
    devdict = device.getdict()
    for f in device._meta.fields:
        devdict[f.name] = device.__dict__.get(f.name) 
    devdict['domain'] = device.domain.id    
    
    getform = getformdevice(device.type)
    form = getform(devdict,instance=device)
    return render_to_response('virt/deviceedit.html', {'device': device,
                                                       'form': form }, 
                                           context_instance=RequestContext(request))        

def delete(request,id):
   device = get_object_or_404(models.Device, pk=id)
   iddomain = device.domain.id
   device.delete()
   request.user.message_set.create(message=_("Device successfully removed"))
   return HttpResponseRedirect(reverse('domain_edit',args=[iddomain]))
                                               
                                                
def save(request):
    
    if request.method == 'POST':
        device = get_object_or_404(models.Device, pk=request.POST.get('id'))
        getform = getformdevice(device.type)
        form = getform(request.POST, instance=device)
        if form.is_valid():
            currentdevice = form.save()
            xml_desc = xmltool.build_device_xml(request.POST)
            if len(xml_desc) > 5:
                currentdevice.xml = xml_desc
                currentdevice.save()
            else:
                currentdevice.delete()
                
            return HttpResponseRedirect(reverse('domain_edit',args=[currentdevice.domain.id]))
        else:
            return render_to_response('virt/deviceedit.html', {'device': device,
                                                               'form': form }, 
                                                   context_instance=RequestContext(request))
            
    
    
            