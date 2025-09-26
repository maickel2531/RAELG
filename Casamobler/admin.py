from django.contrib import admin
from .models import  Rol, Perfil, Usuario, Cliente, Producto, Pedido, Pago, Garantia

admin.site.register(Rol)
admin.site.register(Perfil)
admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(Pago)
admin.site.register(Garantia)

