# -*- coding: utf-8 -*-
import os, sys, random
import virt

# libvirt XML Template 

# General Metadata
# This name should consist only of alpha-numeric characters and is required to be unique within the scope of a single host
# args : 
#  name : name for virtual machine. ( ex: host112 )

def GENERAL_METADATA(type_,name, uuid=None):
    xml = """
<domain type="%s"> 
  <name>%s</name>
""" %(type_,name)
    
    if uuid:
        xml += "  <uuid>%s</uuid>\n" %uuid
    
    return xml    
    

# Basic resources
# args: 
#   memory        : Maximum allocation of memory for the guest at boot time 
# 
#   currentmemory : The actual allocation of memory for the guest. 
#                   This value be less than the maximum allocation, to allow for ballooning up the guests 
#                    memory on the fly. 
#   vcpu          : Number of virtual CPUs allocated for the guest OS.

 
def BASIC_RESOURCE(memory, vcpu, currentMemory=None):

    try:
        memory = int(memory) * 1024
    except:
        pass

    xml = "  <memory>%s</memory>\n" %memory
    if currentMemory:
        try:
            currentMemory = int(int(currentMemory) * 1024)
        except:
            pass
        xml += "  <currentMemory>%s</currentMemory>\n" %currentMemory
    xml += "  <vcpu>%s</vcpu>\n" %vcpu
    return xml 


# Host bootloader
# Hypervisors employing paravirtualization do not usually emulate a BIOS, 
# and instead the host is responsible to kicking off the operating system boot. 
# This may use a pseudo-bootloader in the host to provide an 
# interface to choose a kernel for the guest. An example is pygrub with Xen. 

# args:
#   bootloader  : example: path pygrub ( ex: /usr/bin/pygrub)
#   bootloader_args : exmaple: --append single


def HOST_BOOTLOADER(bootloader=None, bootloader_args=None):
    xml = str()
    if bootloader:
        xml += "  <bootloader>%s</bootloader>\n" %bootloader
        if bootloader_args:
            xml += "  <bootloader_args>%s</bootloader_args>\n"
    
    return xml
    

# Fullyvirtualized guest BIOS boot
# args:
#   type        : example: hvm
#   loader      : path hvmloader ( ex: /usr/lib/xen-3.2-1/boot/hvmloader )
#   boot dev    : hd, cdrom
    
# Paravirtualized guest direct kernel boot
# args: 
#   kernel :  path vmlinuz kernel ( ex: /boot/vmlinuz-2.6.26-2-xen-amd64)
#   initrd :  path initrd kernel  ( ex: /boot/initrd.img-2.6.26-2-xen-amd64)
#   cmdline : options boot  ( ex: root=/dev/sda1 ro console=hvc0 )

def OS_DETAIL(type_,arch=None, machine=None, bootloader=None, loader=None,kernel=None,initrd=None,cmdline=None,boot=None):
    xml = "  <os>\n"
    xml += "    <type"
    
    if arch:
        xml+=""" arch="%s\"""" %arch
    if machine:
        xml +=""" machine="%s\"""" %machine
    xml +=">%s</type>\n" %type_
            
    if loader:
        xml += "    <loader>%s</loader>\n" %loader
    if kernel:
        xml += "    <kernel>%s</kernel>\n" %kernel
    if initrd:
        xml += "    <initrd>%s</initrd>\n" %initrd
    if cmdline:
        xml += "    <cmdline>%s</cmdline>\n" %cmdline
    if boot:
        xml += """    <boot dev="%s"/>\n""" %boot
    xml += "  </os>\n"
    return xml 


# Hypervisor features 
# pae
#    Physical address extension mode allows 32-bit guests to address more than 4 GB of memory.
# acpi
#    ACPI is useful for power management, for example, with KVM guests it is required for graceful shutdown to work.
    
def HYPERVISOR_FEATURES(pae=None,acpi=None,apic=None):
    xml = str()
    if pae or acpi or apic:
        xml = "  <features>\n"
        if pae:
            xml +="    <pae/>\n"
        if acpi:
            xml +="    <acpi/>\n"
        if apic:
            xml +="    <apic/>\n"
        xml += "  </features>\n"
    return xml 

    

# Time keeping
# args:
#     offset :     localtime or utc

def TIME_KEEPING(clock=None):
    if clock: 
        return """  <clock offset="%s"/>\n""" %clock
    return "\n"
    

# Lifecycle control
# args:
#    on_poweroff : destroy
#    on_reboot   : restart
#    on_crash    : restart

def LIFECYCLE_CONTROL(poweroff,reboot,crash):
    xml = "  <on_poweroff>%s</on_poweroff>\n" %poweroff
    xml += "  <on_reboot>%s</on_reboot>\n" %reboot
    xml += "  <on_crash>%s</on_crash>\n" %crash
    return xml


# Devices 
# args:
#     emulator : path of qemu-dm ( ex: /usr/lib/xen-3.2-1/bin/qemu-dm )

def EMULATOR(emulator):
    return "<emulator>%s</emulator>\n" %emulator



# Hard drives, floppy disks, CDROMs 
# args:
#     type :    file or block 
#     device:   disk, floppy, cdrom
#     driver name :  phy , file 
#     source  :   file or dev ( if type  = block, source dev=,  if type = file, source file=)
#                  ex: dev='/dev/lvmxen0/hostXXX-disk'
#     target  dev : sda or sdb or hda or hdc ....
#             bus : ide or scsi 
#     readonly
#     shareable
#     serial : example: <serial>WD-WMAP9A966149</serial>.
#     options : 
#           <encryption type='...'>
#            ...
#           </encryption>

                   
def HARD_DRIVE(type_, device, source, target, target_bus=None, serial=None, readonly=None, \
               shareable=None, driver=None, driver_type=None, driver_cache=None, options=None):
    xml =  """<disk device="%s" type="%s">\n""" %(device,type_)
    
    if driver:
        # driver
        xml += """  <driver name="%s\"""" %driver
        if driver_type:
            xml += """ type="%s\"""" %driver_type
        if driver_cache:
            xml += """ cache="%s\"""" %driver_cache
        xml += "/>\n"
    
    # source
    if type_ == 'file':
        xml += """  <source file="%s"/>\n""" %source
    else:
        xml += """  <source dev="%s"/>\n""" %source    
        
    # target
    xml += """  <target"""
    if target_bus:
        xml += """ bus="%s\"""" %target_bus
    xml += """ dev="%s"/>\n""" %target
    
    if readonly:
        xml += "  <readonly/>\n"
    if shareable:
        xml += "  <shareable/>\n"
    if serial:
        xml += "  <serial>%s</serial>\n" %serial
        
    if options:
        xml +="%s\n" %options
    xml += "</disk>\n"
    
    return xml 
    

# Network interfaces

# Virtual Network
# args : 
#      <target dev='vnet7'/>
#      <mac address="11:22:33:44:55:66"/>

def INTERFACE(type_, source, mac=None, source_port=None, target=None, script=None, model=None):
    xml = """<interface type="%s">\n""" %type_
    
    if type_ in ['bridge','network']:
        xml += """  <source %s="%s"/>\n""" %(type_,source)
    if type_ in ['mcast','server','client']:
        xml += """  <source address="%s\"""" %source
        if source_port:
            xml +=""" port="%s\"""" %source_port
        xml +="/>\n"
    if type_ == 'direct':
        xml += """  <source dev="%s" mode="vepa"/>\n""" %source
    
       
    if mac and type_ in ['bridge','network','user']:
        xml += """  <mac address="%s"/>\n""" %mac
        
    if target:
        xml +="""  <target dev="%s"/>\n""" %target
    if script:
        xml +="""  <script path="%s"/>\n""" %script
    if model:
        xml += """  <model type="%s"/>\n""" %model
    xml += "</interface>\n"
    return xml 



# Input devices

# args: type, bus ( ex : type= mouse, tablet . bus= ps2 or usb )
def INPUT_DEVICE(type_, bus):
    return """<input bus="%s" type="%s"/>\n""" %(bus,type_)

# Graphical framebuffers
# args: port, autoport, listen  (ex: port = -01 or 5901, autoport = yes or no, listen = ip address or 0.0.0.0 )
def GRAPHICAL_VNC(listen,autoport=True,port=None,passwd=None):
    if autoport or port is None:
        port = '-1'
        
    xml = """<graphics"""
    if autoport:
        xml += """ autoport="yes\""""
    xml += """ port="%s\"""" %port or '-1'
    xml += """ listen="%s\"""" %listen
    if passwd:
        xml += """ passwd="%s\"""" %passwd
    xml+=""" type="vnc"/>\n"""
    return xml 
    

# args : autoport = yes or no, multiUser = yes or no
def GRAPHICAL_RDP(autoport=True, multiuser=True):
    xml = """<graphics type="rdp\""""
    if autoport:
        xml += """ autoport="yes\""""
    if multiuser:
        xml += """ multiUser="yes\""""
    xml +="/>\n"
    return xml

def GRAPHICAL_SDL(display=':0.0',fullscreen=True,xauth=None):
    xml += """<graphics type="sdl\""""
    if xauth:
        xml += """ xauth="%s\"""" %xauth
    if fullscreen:
        xml += """ fullscreen="yes\""""
    xml += """ display="%s"/>""" %display
    
# args: source path, target path
# source path='/dev/pts/0 
# target port='0'

def SERIAL_PORT(target,type_='pty',source=None):
    xml = """<serial type="%s">\n""" %type_
    if source:
        xml += """  <source path="%s"/>\n""" %source
    xml += """  <target port="%s"/>\n""" %target
    xml += "</serial>\n"
    
    return xml 
    


# args: sourcepath, target path
# source path='/dev/pts/0 
# target port='0'

def CONSOLE_PORT(target,type_='pty',source=None):
    
    xml = """<console type="%s">\n""" %type_
    if source:
        xml += """  <source path="%s"/>\n""" %source
    xml += """  <target port="%s"/>\n""" %target
    xml += "</console>\n"
    
    return xml



# parallel port 
def PARALLEL_PORT(source,target,type_='pty'):
    xml = """<parallel type="%s">\n""" %type_
    if source:
        xml += """  <source path="%s"/>\n""" %source
    xml += """  <target port="%s"/>\n""" %target
    xml += "</parallel>\n"
    
    return xml


# Sound devices
# Since libvirt 0.4.3
#
# model: 'es1370', 'sb16', and 'ac97' (ac97 since libvirt 0.6.0 )

def SOUND(model):
    return"""
<sound model="%s"/>
""" %model


# Video devices
# model
#    The model element has a mandatory type attribute which 
#    takes the value "vga", "cirrus", "vmvga", "xen" or "vbox". 
#     You can also #provide the amount of video memory in kilobytes using vram and the number of screen with heads. 
# acceleration
#    If acceleration should be enabled (if supported) using the accel3d and accel2d attributes in the acceleration element.

def VIDEO(type_='vga',vram=8192,heads=1,accel3d=True):
    xml = """
<video>
  <model type="%s" vram="%s" heads="%s">
""" %(type_,vram,heads)
    if accel3d:
        xml += """     <acceleration accel3d="yes" accel2d="yes"/>
"""
    xml += "  </model>\n"
    xml += "</video>\n"
    
    return xml 
    

# USB and PCI Devices 
#
# args: vendor id, function id, ex: 0x1234, 0xbeef

def HOSTDEV_USB(vendor,product):
    return """
<hostdev mode="subsystem" type="usb">
    <source>
      <vendor id="%s"/>
      <product id="%s"/>
    </source>
</hostdev>
""" %(vendor,product)


# args : bus, slot, function, ex: bus='0x06', slot='0x02', function='0x0'
def HOSTDEV_PCI(bus,slot,function):
    return """
<hostdev mode="subsystem" type="pci">
     <source>
       <address bus="%s" slot="%s" function="%s"/>
     </source>
</hostdev>
""" %(bus,slot,function)


def CONTROLLER(type_='scsi',index='0', model=None):
    
    xml = """
<controller type="%s" index="%s\"""" %(type_,index)
    if model:
        xml +=""" model="%s\"""" %model
    xml +="/>\n"
    
    return xml 


END_DOMAIN = """</domain>"""

def macgen(amount=50,mtype='xen'):
    """
    Generate random valid MAC address for Domains
    """
    
    # Registered MAC address prefixes
    vmwareprefix='00:50:56:'
    xenprefix='00:16:3E:'
    vboxprefix='08:00:27:'
    qemuprefix='52:54:00:'
    openvzprefix='00:18:51:'
    
    # default xen prefix
    macprefix=xenprefix
    
    # VMWare mac address prefix
    if mtype == 'vmware':
        macprefix=vmwareprefix
    
    # Virtualbox prefix    
    if mtype == 'vbox':
        macprefix=vboxprefix
    
    # QEMU/KVM prefix
    if mtype == 'qemu' or mtype == 'kvm':
        macprefix=qemuprefix
    
    # OpenVZ prefix
    if mtype == 'openvz':
        macprefix=openvzprefix
    
            
    maclist = []
    for iface in virt.models.Device.objects.filter(type='interface'):
        if iface.getdict().get('mac'):
            maclist.append(str(iface.getdict().get('mac')).upper())
               
    macs = []
    for mac in [ ':'.join(['%02x' % random.randint(0,255) for p in range(3)]) for r in range(amount) ]:
        mac = '%s%s' %(macprefix,mac.upper())
        if mac not in maclist:
            macs.append(mac) 
    
    return macs
    
    


