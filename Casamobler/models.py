
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    p_nombrec = models.CharField(max_length=100, null=True, blank=True)
    s_nombrec = models.CharField(max_length=100, null=True, blank=True)
    p_apellidoc = models.CharField(max_length=100, null=True, blank=True)
    s_apellidoc = models.CharField(max_length=100, null=True, blank=True)
    documento_id = models.DecimalField(max_digits=11, decimal_places=0, null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    telefono = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    correo_electronico = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Cliente {self.id}"
    


class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True, verbose_name="ID_Cliente")
    fecha_pedido = models.DateField(null=True, blank=True, verbose_name="Fecha_Pedido")
    fecha_entrega = models.DateField(null=True, blank=True, verbose_name="Fecha_Entrega")
    descripcion_producto = models.CharField(max_length=200, null=True, blank=True, verbose_name="Descripción_Producto")
    cantidad = models.IntegerField(null=True, blank=True, verbose_name="Cantidad")
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="Valor_Unitario")
    valor_total = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="Valor_Total")
    responsable = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Responsable")

    def saldo_pendiente(self):
        total_pagado = sum(
            recibo.valor_abonado or 0
            for recibo in self.recibocaja_set.all()
        )
        if self.valor_total:
            return self.valor_total - total_pagado
        return None
        
    def __str__(self):
        return f"Pedido {self.id}"



class Factura(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_factura = models.DateField(null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    iva = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_factura = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Factura {self.id}"


class Garantia(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True)
    producto = models.CharField(max_length=100, null=True, blank=True)
    motivo_reclamo = models.TextField(null=True, blank=True)
    fecha_reclamo = models.DateField(null=True, blank=True)
    estado_garantia = models.CharField(max_length=30, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Garantía {self.id}"


class ReciboCaja(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_recibo = models.DateField(null=True, blank=True)
    valor_abonado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor_Abonado")
    forma_pago = models.CharField(max_length=30, null=True, blank=True, verbose_name="Forma_Pago")
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente")
    direccion = models.TextField(null=True, blank=True, verbose_name="Dirección")
    concepto = models.CharField(max_length=200, null=True, blank=True, verbose_name="Concepto")

    def saldo_pendiente(self):
        if self.pedido and self.pedido.valor_total and self.valor_abonado:
            # Suma todos los pagos de recibos asociados a este pedido
            total_pagado = sum(
                recibo.valor_abonado or 0
                for recibo in ReciboCaja.objects.filter(pedido=self.pedido)
            )
            return self.pedido.valor_total - total_pagado
        return None

    def __str__(self):
        return f"Recibo {self.id}"


class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_rol

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol.nombre_rol if self.rol else 'Sin rol'}"


class Usuario(models.Model):
    p_nombre = models.CharField(max_length=100, null=True, blank=True)
    s_nombre = models.CharField(max_length=100, null=True, blank=True)
    p_apellido = models.CharField(max_length=100, null=True, blank=True)
    s_apellido = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    correo = models.EmailField(unique=True, null=True, blank=True)
    contraseña = models.CharField(max_length=255, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.p_nombre or f"Usuario {self.id}"
