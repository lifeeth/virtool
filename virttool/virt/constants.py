from django.utils.translation import ugettext as _

# A description of the connection type
VIRT_INTERFACE_NAME = (
    (0, 'Xen'),
    (1, 'QEMU/KVM'),   
    (2, 'VMWare'),
    (3, 'VirtualBox')
)
    

# The Libvirt Connection URI
VIRT_INTERFACE_URI = {
    0: 'xen://%s',
    1: 'qemu://%s/system',
    2: 'esx://%s',
    3: 'vbox+tcp://root@%s/session',
}


DRIVERS_DESCRIPTION =  """

Xen:
    xen:///                          (local access, direct)
    xen+unix:///                     (local access, via daemon)
    xen://host.domain.com/           (remote access, TLS/x509) *Default (node type)
    xen+tcp://host.domain.com/       (remote access, SASl/Kerberos)
    xen+ssh://root@host.domain.com/  (remote access, SSH tunnelled)

QEMU/Kvm: 
    qemu:///session                          (local access to per-user instance)
    qemu+unix:///session                     (local access to per-user instance)

    qemu:///system                           (local access to system instance)
    qemu+unix:///system                      (local access to system instance)
    qemu://host.domain.com/system            (remote access, TLS/x509) *Default (node type)
    qemu+tcp://host.domain.com/system        (remote access, SASl/Kerberos)
    qemu+ssh://root@host.domain.com/system   (remote access, SSH tunnelled)

VMWare    
    vpx://host.domain.com                   (VPX over HTTPS)
    esx://host.domain.com                   (ESX over HTTPS)  *Default (node type)
    gsx://host.domain.com                   (GSX over HTTPS)
    esx://host.domain.com/?transport=http   (ESX over HTTP)
    esx://host.domain.com/?no_verify=1      (ESX over HTTPS, but doesn't verify the server's SSL certificate)
        

VirtualBox:
    vbox:///session                          (local access to per-user instance)
    vbox+unix:///session                     (local access to per-user instance)
    vbox+tcp://user@host.domain.com/session  (remote access, SASl/Kerberos)  *Default (node type) (user=root)
    vbox+ssh://user@host.domain.com/session  (remote access, SSH tunnelled)

"""

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
    (95, _('Reboot by user')),
    (96,_('Powered Off by user')),
    (97,_('Wait Migrate')),
    (98,_('Powered Off')),
    (99,_('Disabled'))
    )



DOM_TYPES = ( ('xen', 'Xen'), 
              ('kvm', 'Kvm') , 
              ('qemu','QEMU'),
              ('vmware','VMWare'),
              ('vbox', 'Virtualbox')
             )



XEN_GUEST_TYPES = (
    ('XEN_PV_DB','XEN - Paravirtualized guest direct kernel boot'),
    ('XEN_PV_BL','XEN - Paravirtualized guest bootloader'),
    ('XEN_FV_DB','XEN - Fullyvirtualized guest direct kernel boot'),
    ('XEN_FV_BB', 'XEN - Fullyvirtualized guest BIOS boot'),
)



OS_TYPES = (  ('hvm', 'HVM - Fully Virtualized'),
              ('linux', 'Linux - Xen PV' ), 
           )
              
BOOT_TYPES_KEYS = ( ('c', 'hd'), ('d', 'cdrom'), ('cd', 'hd,cdrom'), ('dc', 'cdrom,hd'), ('a', 'floppy'), 
               ('n', 'network'), ('ac', 'floppy,hd'), ('an', 'floppy,network'), 
               ('cn', 'hd,network'), ('ad', 'floppy,cdrom'), ('dn', 'cdrom,network'), )
               

BOOT_TYPES = ( ('',''),('hd', 'hd'), ('cdrom', 'cdrom'), ('hd,cdrom', 'hd,cdrom'), ('cdrom,hd', 'cdrom,hd'), ('floppy', 'floppy'), 
              ('network', 'network'), ('floppy,hd', 'floppy,hd'), ('floppy,network', 'floppy,network'), 
              ('hd,network', 'hd,network'), ('floppy,cdrom', 'floppy,cdrom'), ('cdrom,network', 'cdrom,network'), )

               
LIFECYCLE_TYPES = ( ('destroy','destroy'), ('restart','restart'), 
                  ('preserve','preserve'), ('rename-restart','rename-restart') )
CLOCK_TYPES = ( ('utc','utc'),('localtime','localtime') )


DEVICE_TYPES = (
    ('disk', 'Disk'),
    ('controller', 'Controller'),
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

DEVICE_TYPE_LIST = ['disk',
                    'controller',
                    'interface',
                    'graphics',
                    'input',
                    'console',
                    'serial',
                    'parallel',
                    'emulator',
                    'hostdev']

INTERFACE_TYPES = ( ('bridge', 'bridge'), ('network', 'network'),  
                  ('user', 'user'), ('ethernet', 'ethernet'), ('mcast', 'mcast'), 
                  ('server', 'server'), ('direct','direct') )
                  
INTERFACE_MODELS = ( ('',''), ('ne2k_pci','ne2k_pci'),
                     ('i82551','i82551'),('i82557b','i82557b'),
                     ('i82559er','i82559er'),('pcnet','pcnet'),
                     ('rtl8139','rtl8139'),('e1000','e1000'),('virtio','virtio') )
                     

DISK_TYPES = ( ('block', 'block'), ('file', 'file')  )
DISK_DRIVER_CACHE = ( ('default','default'), ('none','none'), ('writethrough','writethrough'), ('writeback','writeback') )

DISKDEV_TYPES = ( ('disk', 'disk'), ('cdrom', 'cdrom'), ('floppy', 'floppy') )
DISKBUS_TYPES = ( ('scsi', 'scsi'), ('ide', 'ide'), ('virtio', 'virtio'), ('xen', 'xen'), ('usb', 'usb') )

GRAPHICTYPES = ( ('vnc','vnc'), 
                 ('sdl','sdl'), 
                 #('rdp','rdp') 
                 )

INPUT_BUS = ( ('usb','usb') , ('ps2','ps2'), ('xen','xen') )
INPUT_TYPES = ( ('mouse','mouse'), ('tablet','tablet') )

VIDEOMODEL_TYPES = (('vga','Vga'), ('cirrus','Cirrus'), ('vmvga','VMVga'), ('xen','Xen'), ('vbox','VBox') )
SOUND_MODELS = ( ('es1370', 'es1370'), ('sb16','sb16'), ('ac97','ac97') )
BOOTLOADER_DEFAULT='/usr/bin/pygrub'

SERIAL_TYPES = ( ('pty','pty'),  # Pseudo TTY   
              ('dev','dev'),     # Host device proxy
              ('pipe','pipe'),   # Named pipe
              ('vc','vc'),       # Virtual console
              ('null','null'),   # Null device
              ('file','file')    # Device logfile
              )

CONSOLE_TYPES = ( ('pty','pty'), # Pseudo TTY 
                  ('stdio','stdio'), # Domain logfile
                  )

PARALLEL_TYPES = ( ('pty','pty') )

                  

# VMWARE SCSI CONTROLLER 
VMWARE_SCSI_CONTROLLER = (
                ('',''),
                ('lsilogic','lsilogic'),  # LSI Logic SCSI controller for recent guests.     
                ('buslogic','buslogic'),  # BusLogic SCSI controller for older guests. 
                ('auto','Auto'), # Auto
                ('lsisas1068','lsisas1068'), # LSI Logic SAS 1068 controller. Since 0.8.0
                ('vmpvscsi','vmpvscsi') # Special VMware Paravirtual SCSI controller, 
                                        # requires VMware tools inside the guest. Since 0.8.3
                )
                
                





