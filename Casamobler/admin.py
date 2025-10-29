from django.contrib import admin
from .models import  Rol, Perfil, Cliente, Producto, Pedido, Pago, Garantia , Remision , DetalleRemision

admin.site.register(Rol)
admin.site.register(Perfil)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(Pago)
admin.site.register(Garantia)
admin.site.register(Remision)
admin.site.register(DetalleRemision)

