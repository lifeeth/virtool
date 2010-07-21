from django.contrib import admin
from virt import models

class NodeAdmin(admin.ModelAdmin):
    fields = ('name','hostname', 'description','capabilities','type', 'active')
    list_display = ('name','hostname', 'description','datecreated','datemodified','active')
    
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name','node','state','datecreated','datemodified')

admin.site.register(models.Domain, DomainAdmin)
admin.site.register(models.Node, NodeAdmin)
admin.site.register(models.Device)
