from django.contrib import admin
from .models import Usuario, Rol, Cliente, Pedido, Factura, Garantia, ReciboCaja

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Rol)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Factura)
admin.site.register(Garantia)
admin.site.register(ReciboCaja)
