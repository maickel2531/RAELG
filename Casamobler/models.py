
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_rol or f"Rol {self.id}"

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol.nombre_rol if self.rol else 'Sin rol'}"


class Usuario(models.Model):
    primer_nombre_usuario = models.CharField(max_length=100, null=True, blank=True)
    segundo_nombre_usuario = models.CharField(max_length=100, null=True, blank=True)
    primer_apellido_usuario = models.CharField(max_length=100, null=True, blank=True)
    segundo_apellido_usuario = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    correo = models.EmailField(unique=True, null=True, blank=True)
    contraseña = models.CharField(max_length=255, null=True, blank=True)
    Rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.primer_nombre_usuario or f"Usuario {self.id}"

class Cliente(models.Model):
    primer_nombre_cliente = models.CharField(max_length=100, null=True, blank=True)
    segundo_nombre_cliente = models.CharField(max_length=100, null=True, blank=True)
    primer_apellido_cliente = models.CharField(max_length=100, null=True, blank=True)
    segundo_apellido_cliente = models.CharField(max_length=100, null=True, blank=True)
    documento_id = models.DecimalField(max_digits=11, decimal_places=0, null=True, blank=True, verbose_name="Documento ID")
    direccion = models.TextField(null=True, blank=True)
    telefono = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    correo_electronico = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Cliente {self.id}"
    
class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100, null=True, blank=True)
    descripcion_producto = models.CharField(max_length=200, null=True, blank=True)
    precio_venta = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)
    costo_unitario = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)

    def __str__(self):
        return self.nombre_producto or f"Producto {self.id}"

class Pedido(models.Model):
    pedido = models.DecimalField(max_digits=11, decimal_places=0, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True, verbose_name="ID_Cliente")
    fecha_pedido = models.DateField(null=True, blank=True, verbose_name="Fecha_Pedido")
    fecha_entrega = models.DateField(null=True, blank=True, verbose_name="Fecha_Entrega")
    cantidad = models.IntegerField(null=True, blank=True, verbose_name="Cantidad")
    responsable = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Responsable")
        
    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente}"

    # Método para calcular el valor total dinámicamente
    def calcular_valor_total(self):
        if self.producto and self.cantidad:
            return self.producto.precio_venta * self.cantidad
        return 0 # O manejar el caso donde producto o cantidad sean None

    # Opcional: Puedes usar una propiedad para acceder fácilmente al total calculado
    @property
    def valor_total(self):
        return self.calcular_valor_total()

class Pago(models.Model):  
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    fecha_pago = models.DateField(null=True, blank=True)
    monto_pago = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Pago {self.id}"
    
    def total_pagado(self):
        pagos = Pago.objects.filter(pedido=self).aggregate(total=Sum('monto_pago'))
        # Si no hay pagos, Sum devuelve None, usamos 0 en ese caso
        return pagos['total'] or 0
    def saldo_pendiente(self):
        # Asegurarse de que valor_total no sea None
        total_pedido = self.valor_total or 0
        return total_pedido - self.total_pagado()

class Garantia(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True)
    motivo_reclamo = models.TextField(null=True, blank=True)
    fecha_reclamo = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Garantía {self.id}"

class Remision(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_emision = models.DateField(auto_now_add=True)
    fecha_entrega_estimada = models.DateField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Remisión #{self.id} - {self.cliente}"

class DetalleRemision(models.Model):
    remision = models.ForeignKey(Remision, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    @property
    def valor_unitario(self):
        return self.producto.precio_venta if self.producto else 0

    @property
    def valor_total(self):
        return self.valor_unitario * self.cantidad
