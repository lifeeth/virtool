from django.utils.translation import ugettext as _

# A description of the connection type
VIRT_INTERFACE_NAME = (
    (0, 'Xen + TLS'),
#    (1, 'Xen + SSH'),
#    (2, 'KVM + TLS'),
#    (3, 'KVM + SSH'),
#    (4, 'Local'),
    )
    

# The Libvirt Connection URI
VIRT_INTERFACE_URI = {
    0: 'xen+tls://%s',
#    1: 'xen+ssh://%s',
#    2: 'qemu+tls://%s/system',
#    3: 'qemu+ssh://%s/system',
#    4: ':///',
}


NODE_STATE = (
    (0, _('No State')),
    (1, _('On')),
    (2, _('Off'))
)

DOMAIN_STATE = (
    (0, _('No State')),
    (1, _('Running')),
    (2, _('Running')),
    (3, _('Paused by user ')),
    (4, _('Being shut down')),
    (5, _('Shut off')),
    (6, _('Crashed')),
    (98,_('Powered Off')),
    (99,_('Disabled'))
    )



DOM_TYPES = ( ('xen', 'xen'), 
             # ('kvm', 'kvm') , 
             # ('qemu','qemu'),
             # ('lxc', 'lxc') 
             )

GUEST_BOOT = (
            ('XEN_PV_DIRECTBOOT','XEN - Paravirtualized guest direct kernel boot'),
            ('XEN_PV_BOOTLOADER','XEN - Paravirtualized guest bootloader'),
            ('XEN_FV_DIRECTBOOT','XEN - Fullyvirtualized guest direct kernel boot'),
            ('XEN_FV_BIOSBOOT', 'XEN - Fullyvirtualized guest BIOS boot'),
            ('QEMU', 'QEMU - QEMU emulated guest on x86_64'),
            ('KVM', 'KVM - KVM hardware accelerated guest on i686'),
)              


OS_TYPES = (  ('linux', 'Linux - Xen PV' ), 
              ('hvm', 'HVM - Fully Virtualized'), 
              #('qemu','QEMU/KVM PV') 
              )
              
BOOT_TYPES_KEYS = ( ('c', 'hd'), ('d', 'cdrom'), ('cd', 'hd,cdrom'), ('dc', 'cdrom,hd'), ('a', 'floppy'), 
               ('n', 'network'), ('ac', 'floppy,hd'), ('an', 'floppy,network'), 
               ('cn', 'hd,network'), ('ad', 'floppy,cdrom'), ('dn', 'cdrom,network'), )
               

BOOT_TYPES = ( ('',''),('hd', 'hd'), ('cdrom', 'cdrom'), ('hd,cdrom', 'hd,cdrom'), ('cdrom,hd', 'cdrom,hd'), ('floppy', 'floppy'), 
              ('network', 'network'), ('floppy,hd', 'floppy,hd'), ('floppy,network', 'floppy,network'), 
              ('hd,network', 'hd,network'), ('floppy,cdrom', 'floppy,cdrom'), ('cdrom,network', 'cdrom,network'), )

               
LIFECYCLE_TYPES = ( ('destroy','destroy'), ('restart','restart'), 
                  ('preserve','preserve'), ('rename-restart','rename-restart') )
CLOCK_TYPES	= ( ('utc','utc'),('localtime','localtime') )


DEVICE_TYPES = (
    ('disk', 'Disk'),
    ('interface','Interface'),
    ('graphics','Graphics'),
    ('parallel','Parallel'),
    ('serial','Serial'),
    ('console','Console'),
    ('channel','Channel'),
    ('emulator','Emulator'),
    ('video','Video'),
    ('sound','Sound'),
    ('input','Input'),
    ('hostdev','Hostdev'),
    
)

INTERFACE_TYPES = ( ('bridge', 'bridge'), ('network', 'network'),  
                  ('user', 'user'), ('ethernet', 'ethernet'), ('mcast', 'mcast'), 
                  ('server', 'server'), ('direct','direct') )
                  
INTERFACE_MODELS = ( ('ne2k_pci','ne2k_pci'),
                     ('i82551','i82551'),('i82557b','i82557b'),
                     ('i82559er','i82559er'),('pcnet','pcnet'),
                     ('rtl8139','rtl8139'),('e1000','e1000'),('virtio','virtio') )
                     

DISK_TYPES = ( ('block', 'block'), ('file', 'file')  )
DISK_DRIVER_CACHE = ( ('default','default'), ('none','none'), ('writethrough','writethrough'), ('writeback','writeback') )

DISKDEV_TYPES = ( ('disk', 'disk'), ('cdrom', 'cdrom'), ('floppy', 'floppy') )
DISKBUS_TYPES = ( ('scsi', 'scsi'), ('ide', 'ide'), ('virtio', 'virtio'), ('xen', 'xen'), ('usb', 'usb') )
GRAPHICTYPES = ( ('vnc','vnc'), ('sdl','sdl'), ('rdp','rdp') )

INPUT_BUS = ( ('usb','usb') , ('ps2','ps2') )
INPUT_TYPES = ( ('mouse','mouse'), ('tablet','tablet') )


VIDEOMODEL_TYPES = (('vga','Vga'),
                    ('cirrus','Cirrus'),
                    ('vmvga','VMVga'),
                    ('xen','Xen'),
                    ('vbox','VBox'))
                    

SOUND_MODELS = ( ('es1370', 'es1370'), ('sb16','sb16'), ('ac97','ac97') )


BOOTLOADER_DEFAULT='/usr/bin/pygrub'


