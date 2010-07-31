from django.db import models
from django import forms 
import virt
from django.utils.translation import ugettext as _
from virt import fields as extrafields
from virt import helpforms

class StrippedCharField(forms.CharField):
    def __init__(self, max_length=None, min_length=None, strip=True, *args, **kwargs):
        super(StrippedCharField, self).__init__(max_length, min_length, *args, **kwargs)
        self.strip = strip

    def clean(self, value):
        if self.strip:
            value = value.strip()
        return super(StrippedCharField, self).clean(value)
        
        
        
class NodeForm(forms.ModelForm):
    class Meta:
        model = virt.models.Node
        fields = ('hostname', 'name','description', 'type','defaultbridge','uri','active')

    
class DomainForm(forms.ModelForm):

    class Meta:
        model = virt.models.Domain             
        exclude = ('state','xml',)
    
    """ Basic resources """
    memory = forms.IntegerField(label=_('Memory'))
    currentMemory = forms.IntegerField(label=_('Current Memory'), required=False)
    vcpu = forms.IntegerField(label=_('Vcpu'),initial=1)

    """ Host bootloader """
    bootloader = forms.CharField(label=_('Boot Loader'),max_length=100, required=False)
    bootloader_args = forms.CharField(label=_('Boot Loader args'), max_length=200, required=False)


    """ OS configuration details """
    os_type = forms.CharField(label=_('OS Type'), widget=forms.Select(choices=virt.models.OS_TYPES))
    os_loader = forms.CharField(label=_('Loader'), max_length=100, required=False, help_text=helpforms.DOMAIN_OS_LOADER)
    os_arch = forms.CharField(label=_('Arch'), max_length=10, required=False, help_text=helpforms.DOMAIN_OS_ARCH)
    os_machine = forms.CharField(label=_('Machine'), max_length=10, required=False, help_text=helpforms.DOMAIN_OS_MACHINE)
    os_kernel = forms.CharField(label=_('Kernel'), max_length=200, required=False, help_text=helpforms.DOMAIN_OS_KERNEL)
    os_initrd = forms.CharField(label=_('Initrd'), max_length=200, required=False, help_text=helpforms.DOMAIN_OS_INITRD)
    os_cmdline = forms.CharField(label=_('Boot cmdline'), max_length=200, required=False, help_text=helpforms.DOMAIN_OS_CMDLINE)
    os_boot = forms.CharField(max_length=30, widget=forms.Select(choices=virt.models.BOOT_TYPES), required=False)

    """ Time keeping """
    clock= forms.CharField(label=_('Clock'), required=False, widget=forms.Select(choices=virt.models.CLOCK_TYPES))
    
    """ Hypervisor features """
    pae = forms.BooleanField(required=False)
    acpi = forms.BooleanField(required=False)
    apic = forms.BooleanField(required=False)
    
    """ Lifecycle control """
    on_poweroff = forms.CharField(label=_('Poweroff'), widget=forms.Select(choices=virt.models.LIFECYCLE_TYPES))
    on_reboot = forms.CharField(label=_('Reboot'), widget=forms.Select(choices=virt.models.LIFECYCLE_TYPES))
    on_crash = forms.CharField(label=_('Crash'), widget=forms.Select(choices=virt.models.LIFECYCLE_TYPES))



    
    
    

#
# DEVICES
#
class DiskForm(forms.ModelForm):
    
    class Meta:
        model = virt.models.Device
        exclude = ('xml','domain','type',)
        
    
    
    disk_type = forms.CharField(label=_('Type'), max_length=5, widget=forms.Select(choices=virt.models.DISK_TYPES))
    device = forms.CharField(label=_('Device'), max_length=6, widget=forms.Select(choices=virt.models.DISKDEV_TYPES))
    source = StrippedCharField(label=_('Source'), max_length=128, help_text=helpforms.DEVICE_DISK_SOURCE)
    target = StrippedCharField(label=_('Target'), max_length=128, help_text=helpforms.DEVICE_DISK_TARGET)
    target_bus = StrippedCharField(label=_('Target Bus'), max_length=10, required=False, \
                                                    help_text=helpforms.DEVICE_DISK_TARGET_BUS)
    driver = StrippedCharField(label=_('Driver'), max_length=10, required=False, help_text=helpforms.DEVICE_DISK_DRIVER)
    driver_type = StrippedCharField(label=_('Driver Type'), max_length=20, required=False)
    driver_cache = StrippedCharField(label=_('Driver Cache'), max_length=20, required=False)
    readonly = forms.BooleanField(label=_('Read only ?'), required=False, initial=False)
    shareable = forms.BooleanField(label=_('Shareable ?'), required=False, initial=False, \
                                help_text=helpforms.DEVICE_DISK_SHAREABLE)
    
    args = forms.CharField(label=_('Args'), widget=forms.Textarea, required=False)
    

class InterfaceForm(forms.ModelForm):
    class Meta:
        model = virt.models.Device
        exclude = ('xml','domain','type',)
        
    interface_type = forms.CharField(label=_('Type'), max_length=20, widget=forms.Select(choices=virt.models.INTERFACE_TYPES))
    source = StrippedCharField(label=_('Source'), max_length=128, required=False, help_text=helpforms.INTERFACE_SOURCE)
    target = StrippedCharField(label=_('Target'), max_length=128, required=False, help_text=helpforms.INTERFACE_TARGET)
    mac = StrippedCharField(label=_('MAc Address'), required=False)
    script = StrippedCharField(label=_('Script Path'), required=False)
    model = forms.CharField(label=_('Model'), required=False, widget=forms.Select(choices=virt.models.INTERFACE_MODELS))
    args = forms.CharField(label=_('Args'), widget=forms.Textarea, required=False)

        
    
    
class GraphicsForm(forms.ModelForm):
    class Meta:
        model = virt.models.Device
        exclude = ('xml','domain','type',)
        
    graphics_type = forms.CharField(max_length=3, widget=forms.Select(choices=virt.models.GRAPHICTYPES))
    sdl_display = forms.CharField(label=_('SDL Display'), max_length=25, required=False)
    sdl_xauth = forms.CharField(label=_('SDL Xauth'), max_length=25, required=False)
    sdl_fullscreen = forms.BooleanField(label=_('SDL FullScreen ?'), required=False)
    autoport = forms.BooleanField(label=_('Auto Port'), required=False, initial=True)
    vnc_port = forms.IntegerField(label=_('VNC Port'), required=False)
    vnc_listen = forms.IPAddressField(label=_('VNC Listen'), initial='0.0.0.0')
    vnc_passwd = forms.CharField(label=_('VNC Password'), required=False)
    

    
class InputForm(forms.ModelForm):
    class Meta:
        model = virt.models.Device
        exclude = ('xml','domain','type',)

        
    input_type = forms.CharField(label=_('Type'),max_length=10, widget=forms.Select(choices=virt.models.INPUT_TYPES))
    bus = forms.CharField(label=_('Bus'), max_length=3, widget=forms.Select(choices=virt.models.INPUT_BUS))

class EmulatorForm(forms.ModelForm):
    class Meta:
        model = virt.models.Device
        exclude = ('xml','domain','type',)
        
    emulator = StrippedCharField(label=_('Emulator'), help_text=helpforms.EMULATOR)
   
    
class SerialForm(forms.ModelForm):
    class Meta:
        model = virt.models.Device
        exclude = ('xml','domain','type',)
    serial_type =  forms.CharField(label=_('Type'),max_length=10, widget=forms.Select(choices=virt.models.SERIAL_TYPES))   
    source = StrippedCharField(label=_('Source Path'), max_length=128, required=False)
    target = forms.IntegerField(label=_('Target Port'), initial=0)   


class ConsoleForm(forms.ModelForm):
    class Meta:
        model = virt.models.Device
        exclude = ('xml','domain','type','xml',)
    console_type =  forms.CharField(label=_('Type'),max_length=10, widget=forms.Select(choices=virt.models.CONSOLE_TYPES))   
    source = StrippedCharField(label=_('Source Path'), max_length=128, required=False)
    target = forms.IntegerField(label=_('Target Port'), initial=0)    


class ParallelForm(forms.ModelForm):
    class Meta:
        model = virt.models.Device
        exclude = ('xml','domain','type',)
    parallel_type =  forms.CharField(label=_('Type'),max_length=10, widget=forms.Select(choices=virt.models.PARALLEL_TYPES))   
    source = StrippedCharField(label=_('Source Path'), max_length=128)
    target = forms.IntegerField(label=_('Target Port'), initial=0)    


# kvm and virtualbox
class HostdevUSBForm(forms.ModelForm):
    class Meta:
        model = virt.models.Device
        exclude = ('xml','domain','type',)
        
    hostdev_type =  forms.CharField(label=_('Type'),initial='usb')       
    vendor = StrippedCharField(label=_('Vendor'), max_length=30)
    product = StrippedCharField(label=_('Product'), max_length=30) 

# kvm and virtualbox
class HostdevPCIForm(forms.ModelForm):
    class Meta:
        model = virt.models.Device
        exclude = ('xml','domain','type',)
    
    hostdev_type =  forms.CharField(label=_('Type'),initial='pci')    
    bus = StrippedCharField(label=_('Bus'), max_length=50)
    slot = StrippedCharField(label=_('Slot'), max_length=50)
    function = StrippedCharField(label=_('Function'), max_length=50)
 

class ControllerForm(forms.ModelForm):
    class Meta:
        model = virt.models.Device
        exclude = ('xml','domain','type',)
    
    controller_type = StrippedCharField(label=_('Type'), max_length=50, initial='scsi')
    index = forms.IntegerField(label=_('Index'), initial=0)
    model = forms.CharField(label=_('Model'),max_length=10, \
                                widget=forms.Select(choices=virt.models.VMWARE_SCSI_CONTROLLER),\
                                required=False) 


class GenericDeviceForm(forms.ModelForm):
    class Meta:
        model = virt.models.Device
        exclude = ('domain',)
    
    xml = forms.CharField(label=_('XML'), widget=forms.Textarea, required=False)
    