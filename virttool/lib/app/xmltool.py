from xml.etree import ElementTree
from xml.dom.minidom import Document, parse, parseString
import libvirttemplate
import copy

def get_domain_dict(XML,exclude=['uuid','devices']):
    domain = {}
    xml = parseString(XML)
    
    textelements = ['name',
                    'uuid',
                    'memory',            
                    'currentMemory',     
                    'vcpu',
                    'bootloader',
                    'bootloader_args',
                    'on_poweroff',
                    'on_reboot',
                    'on_crash']
                    
    featurestaglist = ['pae','acpi','apic']          
    ostaglist = ['type','loader','kernel','initrd','cmdline','boot']
    
    for child0 in xml.childNodes:
        if child0.nodeType == child0.ELEMENT_NODE and child0.localName == "domain":
            
            #domain['domain_id'] = child0.getAttribute("id")
            domain['type'] = child0.getAttribute("type")
            
            for child1 in child0.childNodes:
                
                # remove tag xml 
                if child1.nodeType == child1.ELEMENT_NODE and child1.localName in exclude:
                    child1.parentNode.removeChild(child1)
                
                # basic elements
                if child1.nodeType == child1.ELEMENT_NODE and child1.localName in textelements:
                    
                    if child1.localName in ['memory','currentMemory']:
                        try:
                            # format memory bytes to mbytes 
                            domain[child1.localName] = int(child1.childNodes[0].nodeValue) / 1024
                        except:
                            pass
                    else:
                        try:
                            domain[child1.localName] = child1.childNodes[0].nodeValue
                        except:
                            pass

                
                if child1.nodeType == child1.ELEMENT_NODE and child1.localName == 'features':
                    for ft in child1.childNodes:
                        if ft.nodeType == ft.ELEMENT_NODE and ft.localName in featurestaglist:
                            domain[ft.localName] = True

                
                if child1.nodeType == child1.ELEMENT_NODE and child1.localName == 'clock':
                    domain[child1.localName] = child1.getAttribute('offset') or child1.getAttribute('sync')                
                
                if child1.nodeType == child1.ELEMENT_NODE and child1.localName == "os":
                    for ot in child1.childNodes:
                        if ot.nodeType == ot.ELEMENT_NODE and ot.localName in ostaglist:
                            if ot.localName == 'type':
                                domain['os_%s' %ot.localName] = ot.childNodes[0].nodeValue
                                if ot.getAttribute('arch'):
                                    domain['os_%s' %ot.localName] = ot.getAttribute('arch')
                                if ot.getAttribute('machine'):
                                    domain['os_%s' %ot.localName] = ot.getAttribute('machine')
                            elif ot.localName == 'boot':
                                domain['os_%s' %ot.localName] = ot.getAttribute('dev')
                            else:
                                domain['os_%s' %ot.localName] = ot.childNodes[0].nodeValue       
    return domain
    


def get_device_dict(XML,exclude=[]):
    
    device = {}
    xml = parseString(XML)
    
    for child0 in xml.childNodes:
        
        # exclude 
        if child0.nodeType == child0.ELEMENT_NODE and child0.localName in exclude:
            child0.parentNode.removeChild(child0)
        
        # Disk Device
        if child0.nodeType == child0.ELEMENT_NODE and child0.localName == 'disk':
            device['type'] = child0.localName
            device['disk_type'] = child0.getAttribute('type')
            device['device'] = child0.getAttribute('device')
        
            for child1 in child0.childNodes:
                if child1.nodeType == child1.ELEMENT_NODE and child1.localName == 'driver':
                    device['driver'] = child1.getAttribute('name')
                    if child1.getAttribute('type'):
                        device['driver_type'] = child1.getAttribute('type')
                    if child1.getAttribute('cache'):
                        device['driver_cache'] = child1.getAttribute('cache')
                        
                elif child1.nodeType == child1.ELEMENT_NODE and child1.localName == 'source':
                    if device.get('disk_type') == 'block':
                        device['source'] = child1.getAttribute('dev')
                    else:
                        device['source'] = child1.getAttribute('file')
                elif child1.nodeType == child1.ELEMENT_NODE and child1.localName == 'target':
                    device['target'] = child1.getAttribute('dev')
                    if child1.getAttribute('bus'):
                        device['target_bus'] = child1.getAttribute('bus')
                elif child1.nodeType == child1.ELEMENT_NODE and child1.localName == 'readonly':
                    device['readonly'] = True
                elif child1.nodeType == child1.ELEMENT_NODE and child1.localName == 'shareable':
                    device['shareable'] = True    
                    
                else:
                    device['args'] = child1.toxml()
        

            
                             
        # Interface Device
        if child0.nodeType == child0.ELEMENT_NODE and child0.localName == 'interface':
            device['type'] = child0.localName
            type_ = child0.getAttribute('type')
            device['interface_type'] = type_
            
            for child1 in child0.childNodes:
                if child1.nodeType == child1.ELEMENT_NODE and child1.localName == 'source':
                    if type_ in ['bridge','network']:
                        device[child1.localName] = child1.getAttribute(type_)
                    if type_ in ['mcast','server','client']:
                        device[child1.localName] = child1.getAttribute('address')
                        if child1.getAttribute('port'):
                            device['%s_port' %child1.localName] = child1.getAttribute('port')
                    
                    if type_ == 'direct':
                        device[child1.localName] = child1.getAttribute('dev')
                        device['source_mode'] = 'vepa'
                    
                elif child1.nodeType == child1.ELEMENT_NODE and child1.localName == 'target' \
                    and type_ in ['network','bridge','ethernet']:
                    device['target'] = child1.getAttribute('dev')
                
                elif child1.nodeType == child1.ELEMENT_NODE and child1.localName == 'script':
                    device['script'] = child1.getAttribute('path')
                
                elif child1.nodeType == child1.ELEMENT_NODE and child1.localName == 'model':
                    device['model'] = child1.getAttribute('type')
                
                elif child1.nodeType == child1.ELEMENT_NODE and child1.localName == 'mac':
                    device['mac'] = child1.getAttribute('address').upper()
                else:
                    device['args'] = child1.toxml()


        # Controller (VMWare)
        if child0.nodeType == child0.ELEMENT_NODE and child0.localName == 'controller':
            device['type'] = child0.localName
            device['controller_type'] = child0.getAttribute('type')
            device['index'] = child0.getAttribute('index')
            device['model'] = child0.getAttribute('model')
                                            

        # Hostdev ( virtualbox, KVM )   
        if child0.nodeType == child0.ELEMENT_NODE and child0.localName == 'hostdev':
            device['type'] = child0.localName
            device['mode'] = child0.getAttribute('mode')
            type_ = child0.getAttribute('type')
            device['hostdev_type'] = type_
            
            for child1 in child0.childNodes:
                if child1.nodeType == child1.ELEMENT_NODE and child1.localName == 'source':
                    for child2 in child1.childNodes:
                        if type_ == 'pci':
                            if child2.nodeType == child2.ELEMENT_NODE and child2.localName == 'address':
                                device['bus'] = child2.getAttribute('bus')
                                device['slot'] = child2.getAttribute('slot')
                                device['function'] = child2.getAttribute('function')
                        if type_ == 'usb':
                            if child2.nodeType == child2.ELEMENT_NODE and child2.localName == 'vendor':
                                device['vendor'] = child2.getAttribute('id')
                            if child2.nodeType == child2.ELEMENT_NODE and child2.localName == 'product':    
                                device['product'] = child2.getAttribute('id')
                                
                                
                        
             
                            
        # Emulator
        if child0.nodeType == child0.ELEMENT_NODE and child0.localName == 'emulator':
            try:
                device['type'] = child0.localName
                device['emulator'] = child0.childNodes[0].nodeValue
            except:
                pass
        
        # Graphics
        if child0.nodeType == child0.ELEMENT_NODE and child0.localName == 'graphics':
            device['type'] = child0.localName 
            type_ = child0.getAttribute('type')
            device['graphics_type'] = type_
            if type_ == 'vnc':
                if child0.getAttribute('port'):
                    if child0.getAttribute('port') == '-1':
                        device['vnc_port'] = None
                    else:
                        device['vnc_port'] = child0.getAttribute('port')
                if child0.getAttribute('autoport'):
                    device['autoport'] = True
                if child0.getAttribute('listen'):
                    device['vnc_listen'] = child0.getAttribute('listen')
                else:
                    device['vnc_listen'] = '0.0.0.0'
                    
                device['vnc_passwd'] = child0.getAttribute('passwd')
            
            
        # Input 
        if child0.nodeType == child0.ELEMENT_NODE and child0.localName == 'input':
            device['type'] = child0.localName
            device['input_type'] = child0.getAttribute('type')
            device['bus'] = child0.getAttribute('bus')
            
        
        # Console, Parallel, serial 
        if child0.nodeType == child0.ELEMENT_NODE and child0.localName in ['console','serial','parallel']:
            device['type'] = child0.localName
            device['%s_type' %child0.localName] = child0.getAttribute('type')
            
            
            for child1 in child0.childNodes:
                if child1.nodeType == child1.ELEMENT_NODE and child1.localName == 'source':
                    device['source'] = child1.getAttribute('path')
                if child1.nodeType == child1.ELEMENT_NODE and child1.localName == 'target':
                    device['target'] = child1.getAttribute('port')

        
        # Sound 
        if child0.nodeType == child0.ELEMENT_NODE and child0.localName == 'sound':
            device['type'] = child0.localname
            device['model'] = child0.getAttribute('model')
            
        
        # Video 
        if child0.nodeType == child0.ELEMENT_NODE and child0.localName == 'video':
            device['type'] = child0.localName
            for child1 in child0.childNodes:
                if child1.nodeType == child1.ELEMENT_NODE and child1.localName == 'model':
                    device['video_type'] = child1.getAttribute('type')
                    device['vram'] = child1.getAttribute('vram')
                    device['heads'] = child1.getAttribute('heads')
                    for child2 in child1.childNodes:
                        if child2.nodeType == child2.ELEMENT_NODE and child2.localName == 'acceleration':
                            if child2.getAttribute('accel3d'):
                                device['accel3d'] = child2.getAttribute('accel3d')
                            if child2.getAttribute('accel2d'):
                                device['accel2d'] = child2.getAttribute('accel2d')
                    
        
        
    return device      
    

def get_capabilities_dict(XML, exclude=[]):
    """
      Return python dict from XML libvirt
    """
    
    capabilities = {}
    
    try:
        xml = ElementTree.fromstring(XML)
    
    
        # cpus available
        capabilities['cpus'] = xml.findall('.//cpus')[0].get('num') if xml.findall('.//cpus') else 1

        # live migration support
        capabilities['live_migration'] = True if xml.findall('.//migration_features/live') else False 

        # guest available 
        capabilities['guest'] = []
        for guest in xml.findall('guest'):
            guestdic = {}
    
            # arch 
            guestdic['arch'] = guest.find('arch').get('name') if guest.find('arch') else None
    
            # domain type
            guestdic['domain_type'] = guest.findall('.//domain')[0].get('type') if guest.findall('.//domain') else None

            # get os_type, machine, emulator 
            for tagsel in ['os_type','machine','emulator','wordsize','loader']:
                guestdic[tagsel] = guest.findall('.//%s' %tagsel)[0].text if guest.findall('.//%s' %tagsel) else None
    
            # features acpi, apic, pae, nonpae
            guestdic['features_acpi'] = True if guest.findall('.//features/acpi') else None
            guestdic['features_apic'] = True if guest.findall('.//features/apic') else None
            guestdic['features_pae'] = True if guest.findall('.//features/pae') else None
            guestdic['features_nonpae'] = True if guest.findall('.//features/nonpae') else None
        
            capabilities['guest'].append(guestdic)
    except:
        print "capabilities invalid xml"
            

        
    return capabilities    

            
    
    
def getxml(libvirtxml,options=None):
    """
      format xml attributes 
    """
    newxml = parseString(libvirtxml)
    newxml.firstChild.removeAttribute('id')
    
    typedomain = newxml.firstChild.getAttribute('type')
    
    devices = []

    devt = ['disk',
            #'interface',
            'graphics',
            'parallel',
            'serial',
            #'console',
            'channel',
            'emulator',
            'video',
            'sound',
            'input',
            'hostdev']




    for child0 in newxml.childNodes:
        for child1 in child0.childNodes:

            # remove uuid
            if child1.nodeType == child1.ELEMENT_NODE and child1.localName == "uuid":
                child1.parentNode.removeChild(child1)


            # 
            # DEVICES
            #    
            if child1.nodeType == child1.ELEMENT_NODE and child1.localName == "devices":
                for dev in child1.childNodes:     

                    if dev.nodeType == dev.ELEMENT_NODE and dev.localName in devt:
                        devices.append(dict(type=dev.localName,xml=dev.toxml()))

                    if dev.nodeType == dev.ELEMENT_NODE and dev.localName  == 'interface':
                        bridgedetected=False
                        typeinterface = dev.getAttribute('type')
                        
                        # remove target - interface 
                        for devinter in dev.childNodes:
                            if devinter.nodeType == devinter.ELEMENT_NODE and devinter.localName == 'source':
                                bridgedetected=True
                                
                            if devinter.nodeType == devinter.ELEMENT_NODE and devinter.localName == 'target':
                                devinter.parentNode.removeChild(devinter)
                        
                        if bridgedetected == False and typeinterface == 'bridge' and typedomain == 'xen':
                            xml_ = str()
                            interfacedict = get_device_dict(dev.toxml())
                            fiximport = False
                            if options:
                                if options.get('defaultbridge'):
                                    fiximport = True                                
                                    if interfacedict.get('mac'):
                                        xml_ = libvirttemplate.INTERFACE('bridge', options.get('defaultbridge'),interfacedict.get('mac'))
                                    else:
                                        macgen = libvirttemplate.macgen(50,typedomain)
                                        xml_ = libvirttemplate.INTERFACE('bridge',options.get('defaultbridge'), macgen[0])
                            if fiximport == True:        
                                devices.append(dict(type='interface',xml=xml_))
                            else:
                                devices.append(dict(type='interface',xml=dev.toxml()))
                                            
                        else:
                            devices.append(dict(type='interface',xml=dev.toxml()))
                # remove devices
                child1.parentNode.removeChild(child1)

    return dict(type=typedomain, domain=newxml.toxml(),devices=devices)
          
    
def build_domain_xml(dom,exclude=[]):
    xml = str()
    
    xml += libvirttemplate.GENERAL_METADATA(dom.get('type'), dom.get('name'))
    xml += libvirttemplate.BASIC_RESOURCE(dom.get('memory'),dom.get('vcpu'),dom.get('currentMemory'))
    xml += libvirttemplate.HOST_BOOTLOADER(dom.get('bootloader'),dom.get('bootloader_args'))
    xml += libvirttemplate.OS_DETAIL(dom.get('os_type'),
                                     dom.get('os_arch'),
                                     dom.get('os_machine'),
                                     dom.get('bootloader'),
                                     dom.get('os_loader'),
                                     dom.get('os_kernel'),
                                     dom.get('os_initrd'),
                                     dom.get('os_cmdline'),
                                     dom.get('os_boot'))                                     
    xml += libvirttemplate.TIME_KEEPING(dom.get('clock'))   
    xml += libvirttemplate.HYPERVISOR_FEATURES(dom.get('pae'),dom.get('acpi'),dom.get('apic')) 
    xml += libvirttemplate.LIFECYCLE_CONTROL(dom.get('on_poweroff'),dom.get('on_reboot'),dom.get('on_crash'))
    xml += libvirttemplate.END_DOMAIN

    
    return xml
      
def build_device_xml(dev,exclude=[]):
    xml = str()
    if dev.get('type') == 'disk':
        xml += libvirttemplate.HARD_DRIVE(dev.get('disk_type'),
                                          dev.get('device'),
                                          dev.get('driver'),
                                          dev.get('source'),
                                          dev.get('target'),
                                          dev.get('serial'),
                                          dev.get('readonly'),
                                          dev.get('shareable'),
                                          dev.get('driver_type'),
                                          dev.get('target_bus'),
                                          dev.get('driver_cache'),
                                          dev.get('options'))
                                          
    
    if dev.get('type') == 'interface':
        xml += libvirttemplate.INTERFACE(dev.get('interface_type'), 
                                         dev.get('source'), 
                                         dev.get('mac'),
                                         dev.get('source_port'),
                                         dev.get('target'),
                                         dev.get('script'),
                                         dev.get('model'))
    if dev.get('type') == 'emulator':
        xml += libvirttemplate.EMULATOR(dev.get('emulator'))
        
        
    if dev.get('type') == 'graphics':
        if dev.get('graphics_type') == 'vnc':
            xml += libvirttemplate.GRAPHICAL_VNC(dev.get('vnc_listen'),
                                                 dev.get('autoport'),
                                                 dev.get('vnc_port') or '-1', 
                                                 dev.get('vnc_passwd'))
        if dev.get('graphics_type') == 'sdl':
            xml += libvirttemplate.GRAPHICAL_SDL(dev.get('sdl_display'),
                                                 dev.get('sdl_fullscreen'),
                                                 dev.get('sdl_xauth'))
        
                                                     
                                                         
    
    if dev.get('type') == 'input':
        xml += libvirttemplate.INPUT_DEVICE(dev.get('input_type'),dev.get('bus'))    
    if dev.get('type') == 'serial':
        xml += libvirttemplate.SERIAL_PORT(dev.get('target'), dev.get('serial_type'),dev.get('source'))
    if dev.get('type') == 'console':
        xml += libvirttemplate.CONSOLE_PORT(dev.get('target'), dev.get('console_type'), dev.get('source'))
    if dev.get('type') == 'parallel':
        xml += libvirttemplate.PARALLEL_PORT(dev.get('target'), dev.get('parallel_type'), dev.get('source'))
        
                         
    return xml 
                
