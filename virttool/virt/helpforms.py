from django.utils.translation import ugettext as _

NODE_HOSTNAME = _("Example: server01.domain.com, 10.2.10.123, ....")
NODE_TYPE= _("Another method of connection other than TLS, specify the URI field")
NODE_DEFAULTBRIDGE = _("Default bridge to import and transport domain with different interface. Example: bridge0, xenbr0, ...")
DOMAIN_BOOTLOADER = _("This may use a pseudo-bootloader in the host to provide an interface to choose a kernel for the guest. An example is pygrub with Xen.")
DOMAIN_BOOTLOADER_ARGS = _("Optional. Example: --append single")

DOMAIN_OS_ARCH = _("x86_64, i686. Optional")
DOMAIN_OS_LOADER = _("it is only needed by Xen fully virtualized domains. Example: /usr/lib/xen-3.2-1/boot/hvmloader")
DOMAIN_OS_MACHINE = _("pc, xenpv,...")
DOMAIN_OS_KERNEL = _("Example: /boot/vmlinuz-2.6.26-2-xen-amd64")
DOMAIN_OS_INITRD = _("Example: /boot/initrd.img-2.6.26-2-xen-amd64")
DOMAIN_OS_CMDLINE =  _('Example: root=/dev/sda2 ro, root=/dev/sda2 ro console=hvc0')


DEVICE_DISK_SOURCE = _('Ex Path: /dev/lvm0/machine00-disk, /var/lib/libvirt/images/demo2.img, /home/user/tmp/vbox.vdi, [local-storage] Fedora11/Fedora11.vmdk ')
DEVICE_DISK_TARGET = _('Valid types: sda, sdb, hda, sda1, sda2, hda2 ....')
DEVICE_DISK_TARGET_BUS = _('scsi, ide, xen. Optional')
DEVICE_DISK_DRIVER = _('phy, file, tap. Optional')
DEVICE_DISK_SHAREABLE = _('Shared between domains (assuming the hypervisor and OS support this)')


INTERFACE_SOURCE = _('Interface, ex: eth0, bridge0, default, VM Network,....')
INTERFACE_TARGET = _('Optional. vnet1, vif0, vif2, ...')

EMULATOR = _("Ex: /usr/bin/qemu, /usr/lib/xen/bin/qemu-dm, /usr/bin/qemu-kvm")
