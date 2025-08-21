from django.contrib import admin
from .models import Usuario, Rol, Cliente, Pedido, Factura, Garantia, ReciboCaja

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Rol)